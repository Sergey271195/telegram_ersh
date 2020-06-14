from django.contrib import admin
from django.urls import path, include
from .webhook import Webhook

Webhook().setWebhook()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ershbot_api.urls'), name = 'ershapi')
]
