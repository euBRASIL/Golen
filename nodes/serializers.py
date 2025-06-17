from rest_framework import serializers
from .models import Node

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'ip', 'location', 'status', 'last_update']
        read_only_fields = ['id', 'last_update', 'status'] # Status updated by specific endpoint

class NodeRegistrationSerializer(serializers.ModelSerializer):
    # Used for /api/register - only ip and location are provided by the node
    class Meta:
        model = Node
        fields = ['ip', 'location']
        # id, status, last_update will be set by the server

class NodeStatusUpdateSerializer(serializers.Serializer):
    # Not a ModelSerializer as we might not directly map to all model fields initially
    # Or we can use ModelSerializer with specific fields if node sends its ID
    node_id = serializers.UUIDField(required=False) # If not in URL
    status = serializers.ChoiceField(choices=[('online', 'Online'), ('offline', 'Offline')])
    # task_result = serializers.CharField(required=False, allow_blank=True) # For future use
