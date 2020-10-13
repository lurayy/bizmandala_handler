from django.urls import path
from erp import views

urlpatterns = [
    path('erps/get',  views.Container.as_view()),
]