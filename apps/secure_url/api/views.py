from django.db import connection
from django.shortcuts import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import SecuredEntitySerializer
from ..constants import SecuredEntityTypes
from ..models import SecuredEntityAccessLog, SecuredEntity


class SecuredEntityCreateListRetrieveApiViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = SecuredEntitySerializer

    def get_queryset(self):
        return SecuredEntity.objects.filter(user=self.request.user)


class SecuredEntityRegeneratePasswordApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        secured_entity = get_object_or_404(SecuredEntity, pk=pk, user=request.user)
        secured_entity.regenerate_password()
        return Response(SecuredEntitySerializer(secured_entity).data)


class SecuredEntityStatsApiView(APIView):
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
                daily_stats = stats.setdefault(stat_item[0], {SecuredEntityTypes.FILE: 0,
                                                              SecuredEntityTypes.LINK: 0})
                daily_stats[stat_item[1]] = stat_item[2]

        return stats

    def get(self, request):
        return Response(self._prepare_stats())
