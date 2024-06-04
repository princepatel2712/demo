from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('int.urls')),
    path('v2/', include('app.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
