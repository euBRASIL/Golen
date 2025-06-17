from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView # For simple static pages if needed
from django.contrib.auth import views as auth_views # For login/logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'), # Redirect to index after logout
    # Dashboard will be handled by nodes.views, so include nodes.urls for that
    # path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'), # Placeholder, will be replaced
    path('', include('nodes.urls')), # App urls for 'nodes' app
    # Potentially API urls will be under nodes.urls or their own include
]
