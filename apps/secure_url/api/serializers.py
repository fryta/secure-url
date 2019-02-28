from rest_framework import serializers

from ..models import SecuredEntity


class SecuredEntitySerializer(serializers.ModelSerializer):
    access_url = serializers.SerializerMethodField()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def get_access_url(self, obj):
        # TODO: add it
        return 'aaa'

    class Meta:
        model = SecuredEntity
        fields = ('id', 'url', 'file', 'type', 'created', 'password', 'is_accessible', 'access_url')
        read_only_fields = ('type', 'created', 'password', 'is_accessible', 'access_url')
        extra_kwargs = {
            'url': {'write_only': True},
            'file': {'write_only': True}
        }


class SecuredEntitySerializerRegeneratePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate_password(self, *args, **kwargs):
        import pdb
        pdb.set_trace()
        pass
