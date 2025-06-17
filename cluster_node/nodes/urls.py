from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('api/nodes/', views.NodeListAPIView.as_view(), name='api-node-list'),
    path('api/register/', views.NodeRegisterAPIView.as_view(), name='api-node-register'),
    path('api/task/', views.NodeTaskAPIView.as_view(), name='api-node-task'),
    path('api/status/', views.NodeStatusUpdateAPIView.as_view(), name='api-node-status'),
]
