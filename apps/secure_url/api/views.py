from django.db import connection
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import SecuredEntitySerializer, SecuredEntityAccessSerializer
from ..constants import SecuredEntityTypes
from ..models import SecuredEntityAccessLog, SecuredEntity


class SecuredEntityCreateListRetrieveApiViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Api view set to: create, retrieve, list secured entities.

    @:param id - primary key of secured entity item
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SecuredEntitySerializer

    def get_queryset(self):
        return SecuredEntity.objects.filter(user=self.request.user)


class SecuredEntityAccessApiView(APIView):
    """
    Restricts or grants the access to the secured entity.

    @:param id - primary key of secured entity item
    @:param password - password for specific secured entity
    """
    permission_classes = (AllowAny,)

    def post(self, request, pk):
        secured_entity = get_object_or_404(SecuredEntity, pk=pk)

        access_serializer = SecuredEntityAccessSerializer(data=request.data, context={'secured_entity': secured_entity})
        access_serializer.is_valid(raise_exception=True)

        SecuredEntityAccessLog.objects.create(secured_entity=secured_entity)

        return Response({'secured_entity': request.build_absolute_uri(secured_entity.get_redirect_url())})


class SecuredEntityRegeneratePasswordApiView(APIView):
    """
    Regenerates password for a secured entity.

    @:param id - primary key of secured entity item
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        secured_entity = get_object_or_404(SecuredEntity, pk=pk, user=request.user)
        secured_entity.regenerate_password()
        return Response(SecuredEntitySerializer(secured_entity).data)


class SecuredEntityStatsApiView(APIView):
    """
    Generates the stats for number of unique visits for links or files.
    """
    permission_classes = (IsAuthenticated,)

    def _prepare_stats(self):
        # Since there is no proper support for GROUP BY in django ORM the raw query is used here.
        # Its efficient but could be risky while changing database engine.
        raw_query = """
            SELECT
                DATE({secured_entity_access_log_table}.created) as created_date,
                {secured_entity_table}.type as type,
                COUNT(DISTINCT {secured_entity_access_log_table}.secured_entity_id)
            FROM {secured_entity_access_log_table}
            JOIN {secured_entity_table} ON {secured_entity_table}.id = {secured_entity_access_log_table}.secured_entity_id
            GROUP BY created_date, type
            ORDER BY created_date;
        """.format(secured_entity_table=SecuredEntity._meta.db_table,
                   secured_entity_access_log_table=SecuredEntityAccessLog._meta.db_table)

        stats = {}
        with connection.cursor() as cursor:
            cursor.execute(raw_query)

            for stat_item in cursor.fetchall():
                # required because in Heroku stat_item[0] is a datetime.date object...
                date = stat_item[0] if isinstance(stat_item[0], str) else stat_item[0].strftime('%Y-%m-%d')

                daily_stats = stats.setdefault(date, {SecuredEntityTypes.FILE: 0,
                                                      SecuredEntityTypes.LINK: 0})
                daily_stats[stat_item[1]] = stat_item[2]

        return stats

    def get(self, request):
        return Response(self._prepare_stats())
