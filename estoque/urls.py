from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
from django.contrib.auth import views as auth_views
urlpatterns = [path('api/', include('core.api_urls')), path('api-auth/', include('rest_framework.urls')), path('login/',auth_views.LoginView.as_view(template_name='core/login.html'),name='login'),path('logout/',auth_views.LogoutView.as_view(),name='logout')] + urlpatterns
