from django.urls import path
from erp import views

urlpatterns = [
    path('get',  views.Container.as_view()),
]