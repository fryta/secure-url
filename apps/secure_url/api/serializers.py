from rest_framework import serializers
from rest_framework.reverse import reverse

from ..models import SecuredEntity
from ..validators import validate_secured_entity


class SecuredEntitySerializer(serializers.ModelSerializer):
    access_url = serializers.SerializerMethodField()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def get_access_url(self, obj):
        return self.context['request'].build_absolute_uri(
            reverse('secure_url.api:secured-entity-get-access-api-view', args=(obj.pk,)))

    class Meta:
        model = SecuredEntity
        fields = ('id', 'url', 'file', 'type', 'created', 'password', 'is_accessible', 'access_url')
        read_only_fields = ('type', 'created', 'password', 'is_accessible', 'access_url')
        extra_kwargs = {
            'url': {'write_only': True},
            'file': {'write_only': True}
        }


class SecuredEntityAccessSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate(self, data):
        validate_secured_entity(data, self.context['secured_entity'])
        return data
