from django.urls import path
from . import views

app_name='air_quality'

urlpatterns = [
    path('get_air_quality/', views.get_air_quality, name='get_air_quality'),
    path('test/', views.test),
]