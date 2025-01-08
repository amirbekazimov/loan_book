from django.urls import path
from .views import DebtListCreateView, DebtDetailView, MyDebtsView

urlpatterns = [
    # path('register/', RegisterUserView.as_view(), name='register_user'),
    path('debts/', DebtListCreateView.as_view(), name='debt-list-create'),
    path('debts/<int:pk>/', DebtDetailView.as_view(), name='debt-detail'),
    path('my-debts/', MyDebtsView.as_view(), name='my-debts'),
]
