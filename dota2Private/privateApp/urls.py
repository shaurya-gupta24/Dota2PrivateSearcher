from django.urls import path
from privateApp import views

urlpatterns = [
    path('',views.home, name="home")
]
