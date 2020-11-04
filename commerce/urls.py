from django.urls import path
from . import views
from . import transactions
urlpatterns = [
    path('settings',views.SettingView.as_view()),
    path('', transactions.InvoiceView.as_view()),
    path('<str:uuid>', transactions.InvoiceView.as_view()),
    path('credits/', transactions.CreditView.as_view()),
    path('credits/<str:uuid>', transactions.CreditView.as_view()),
    
]