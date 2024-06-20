from rest_framework import serializers


class CreateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField()
    is_active = serializers.BooleanField(default=True)

class CreateCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
