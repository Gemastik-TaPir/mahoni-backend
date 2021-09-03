from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/', include('api.root.authentication.urls', namespace='auth'))
]