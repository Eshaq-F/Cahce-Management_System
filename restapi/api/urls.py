from django.urls import path
from django.contrib.auth.views import LogoutView

from api.views import (
    TransactionListCreateView,
    TransactionRetrieveUpdateDeleteView,
    UserRegistrationView,
    UserLogoutView
)

urlpatterns = [
    path('transactions/', TransactionListCreateView.as_view(), name='list-create'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDeleteView.as_view(), name='retrieve-update-delete'),
    path('api/auth/', UserRegistrationView.as_view(), name='user-login-register'),
    path('api/logout/', UserLogoutView.as_view(), name='user-logout'),
]
