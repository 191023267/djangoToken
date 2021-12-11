from django.urls import path, include
from . import views

urlpatterns = [
    path('users/', views.AuthView.as_view()),
    path('order/', views.OrderView.as_view()),
]
