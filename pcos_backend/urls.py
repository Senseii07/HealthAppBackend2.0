from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/wellness/', include('apps.wellness.urls')),
    path('api/content/', include('apps.content.urls')),
    path('api/chat/', include('apps.chat.urls')),
]
