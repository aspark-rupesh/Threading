from django.urls import path
from .views import async_index_api

urlpatterns = [
    path('index/', async_index_api , name="index"),

]