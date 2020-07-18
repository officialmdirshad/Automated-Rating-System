from django.urls import path, include
from .views import SentimentAPI
urlpatterns = [
    path('status/', SentimentAPI.as_view(), name='deno'),
]
