from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Node
from .serializers import NodeSerializer, NodeRegistrationSerializer, NodeStatusUpdateSerializer

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

@login_required
def dashboard_view(request):
    nodes = Node.objects.all()
    return render(request, 'dashboard.html', {'nodes': nodes, 'user': request.user})

# API Views

class NodeListAPIView(generics.ListAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]

class NodeRegisterAPIView(generics.CreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeRegistrationSerializer
    permission_classes = [AllowAny] # Nodes should be able to register themselves

    def perform_create(self, serializer):
        # Set status to 'online' upon registration and save
        serializer.save(status='online')

class NodeTaskAPIView(views.APIView):
    permission_classes = [AllowAny] # Or some node authentication

    def get(self, request, *args, **kwargs):
        # Example task
        task_data = {
            'task_id': 'task_123',
            'type': 'simple_math',
            'instruction': 'Add the numbers.',
            'data': {
                'a': 10,
                'b': 25
            }
        }
        return Response(task_data, status=status.HTTP_200_OK)

class NodeStatusUpdateAPIView(views.APIView):
    permission_classes = [AllowAny] # Or some node authentication

    def post(self, request, *args, **kwargs):
        # Expects node_id (or ip) and new status in request.data
        # For now, let's assume 'ip' is sent by the node for identification
        node_ip = request.data.get('ip')
        new_status = request.data.get('status')

        if not node_ip or not new_status:
            return Response({'error': 'IP and status are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            node = Node.objects.get(ip=node_ip)
            # Validate status
            if new_status not in ['online', 'offline']:
                 return Response({'error': 'Invalid status value.'}, status=status.HTTP_400_BAD_REQUEST)
            node.status = new_status
            # last_update is auto_now, so it will be updated on save
            node.save(update_fields=['status', 'last_update'])
            return Response(NodeSerializer(node).data, status=status.HTTP_200_OK)
        except Node.DoesNotExist:
            return Response({'error': 'Node not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
