from django.urls import path
from .views import ErshApiView


urlpatterns = [
    path('', ErshApiView().dispatch)
]