from django.urls import path
from erp import views

urlpatterns = [
    path('get',  views.Container.as_view()),
    path('view/list', views.list_erps),
    path('view/new', views.register_erp),
    path('new', views.create)
]