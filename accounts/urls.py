from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import AccountListCreateView, AccountDetailView, deposit, withdraw, transfer, TransactionListView, \
    CustomerViewSet

router = DefaultRouter()

router.register(r"customers", CustomerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('accounts/', AccountListCreateView.as_view(), name='account-list'),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('accounts/<int:pk>/deposit/', deposit, name='account-deposit'),
    path('accounts/<int:pk>/withdraw/', withdraw, name='account-withdraw'),
    path('accounts/transfer/', transfer, name='account-transfer'),
    path('accounts/<int:pk>/transactions/', TransactionListView.as_view(), name='transaction-list'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
