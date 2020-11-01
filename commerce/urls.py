from django.urls import path
from . import views

urlpatterns = [
    path('bundles',views.BundleClassView.as_view()),
    path('bundles/<str:uuid>',views.BundleClassView.as_view()),
    path('prices',views.PriceView.as_view()),
    path('prices/<str:uuid>',views.PriceView.as_view()),
    # path('invoices')
]