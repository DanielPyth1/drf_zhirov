
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('lms.urls')),
    path('api/', include('users.urls')),
    path('', lambda request: redirect('api/')),
]