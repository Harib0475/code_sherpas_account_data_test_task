from django.urls import path
from .views import AccountListCreateView, AccountDetailView, deposit, withdraw, transfer, TransactionListView

urlpatterns = [
    path('accounts/', AccountListCreateView.as_view(), name='account-list'),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('accounts/<int:pk>/deposit/', deposit, name='account-deposit'),
    path('accounts/<int:pk>/withdraw/', withdraw, name='account-withdraw'),
    path('accounts/transfer/', transfer, name='account-transfer'),
    path('accounts/<int:pk>/transactions/', TransactionListView.as_view(), name='transaction-list'),
]
