from django.urls import path
from erp import views

urlpatterns = [
    path('', views.ERPView.as_view()),
    path('<str:uuid>', views.ERPView.as_view()),
    path('<str:uuid>/stop', views.stop_container),
    path('<str:uuid>/start', views.start_container)
]