from rest_framework import serializers
from .models import Node

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'ip', 'location', 'status', 'last_update']
        read_only_fields = ['id', 'last_update']

class NodeRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['ip', 'location']

class NodeStatusUpdateSerializer(serializers.Serializer):
    node_id = serializers.UUIDField(required=False)
    status = serializers.ChoiceField(choices=[('online', 'Online'), ('offline', 'Offline')])
