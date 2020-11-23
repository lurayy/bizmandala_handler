from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserBaseView.as_view()),
    path('register', views.register_new_user),
]
