from django.urls import path

from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [

    path('',views.seriesHome,name='seriesHome'),
    path("series/<slug>", views.seriesPage, name='seriesHome'),
    path("search", views.search, name="search"),
    path("login/", views.loginPage, name="login"),
    path("register/", views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="login/password_reset.html"), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="login/password_reset_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="login/password_reset_done.html"), name="password_reset_complete"),
    path('c', views.index, name="index"),
    path('<str:room>/', views.room, name="room"),
    path('checkview', views.checkview, name="checkview"),
    path('send', views.send, name="send"),
    path('getMessages/<str:room>/', views.getMessages, name="getMessages"),
    path('game', views.game, name="game"),
    path('labs', views.labs, name="labs"),
    path('question', views.question, name="question"),
    path('profile', views.profile, name="profile"),
    path('wordbeater', views.wordbeater, name="wordbeater"),

    # path("", views.home, name="home"),
    # path("movie/<slug>", views.moviePage, name="moviepage"),
    # path("", views.seriesHome, name="seriesHome"),
]
