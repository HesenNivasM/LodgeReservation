from django.urls import path
from . import views

urlpatterns = [
    path('book', views.book, name="book" ),
    path('rooms', views.rooms, name="rooms" ),
    path('', views.index, name="index" ),
]
