from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('hajsjdjfkasxadm/', admin.site.urls),
    path('', include('webswap.urls')),
]
