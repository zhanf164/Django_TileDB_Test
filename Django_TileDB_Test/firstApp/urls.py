from django.urls import path

from firstApp import views

urlpatterns = [
    path("", views.LoginPage, name="LoginPage"),
    path("LandingPage", views.LandingPage, name="LandingPage") 
]