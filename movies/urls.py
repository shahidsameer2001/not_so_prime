from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("movie/<slug>", views.moviePage, name="moviepage"),
    path("series/", views.seriesHome, name='seriesHome'),
    path("series/<slug>", views.seriesPage, name='seriesHome'),
    path("search", views.search, name="search"),
    path('c', views.index, name="index"),
    path('<str:room>/', views.room, name="room"),
    path('checkview', views.checkview, name="checkview"),
    path('send', views.send, name="send"),
    path('getMessages/<str:room>/', views.getMessages, name="getMessages")
]
