from django.urls import path
from . import views

urlpatterns = [
    path('', views.token_list, name='token_list'),
]