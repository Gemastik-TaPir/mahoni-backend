from django.urls import path
from api_air_quality import views

app_name='api_air_quality'

urlpatterns = [
    path('air_quality/', views.air_quality_list),
    path('air_quality_detail/<int:pk>/', views.air_quality_detail),
]