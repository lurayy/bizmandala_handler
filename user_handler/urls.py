from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserBaseView.as_view())
]
