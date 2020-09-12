from django.urls import path
from .views import  index_name, delete_city

urlpatterns = [
    path('', index_name, name = 'indexo'),
    path('/delete/<city_name>/', delete_city, name = 'delete_city')
]