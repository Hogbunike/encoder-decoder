from rest_framework import serializers

class EncodeDecodeSerializer(serializers.Serializer):
    payload = serializers.CharField()
    salt_key = serializers.CharField()
    salt_index = serializers.IntegerField()
    encoded_payload = serializers.CharField(required=False)
