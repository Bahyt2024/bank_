from django.urls import path
from . import views

urlpatterns = [
    path('account/create/', views.CreateAccountView.as_view()),
    path('account/<int:pk>', views.GetAccountView.as_view()),
    path('account/<int:pk>/update', views.UpdateAccountView.as_view()),
    path('accounts', views.GetAllAccountsView.as_view()),

    path('credit/create', views.CreateCreditView.as_view()),
    path('credit/<int:pk>', views.GetCreditView.as_view()),
    path('credit/<int:pk>/update', views.UpdateCreditView.as_view()),
    path('credits', views.GetAllCreditsView.as_view()),

    path('transaction/transfer', views.TransferView.as_view()),
    path('transaction/<int:pk>', views.GetTransactionByIdView.as_view()),
    path('transactions', views.GetTransactionsView.as_view()),
    path('transaction/<int:pk>/cancel', views.CancelTransactionView.as_view()),

    path('report/transactions', views.TransactionsReportView.as_view()),
    path('report/financial-summary', views.FinancialSummaryView.as_view()),

    # path('admin/block-user', views.BlockUserView.as_view()),
    # path('admin/unblock-user', views.UnblockUserView.as_view()),
    # path('admin/users', views.ListUsersView.as_view()),
    # path('admin/set-role', views.SetUserRoleView.as_view()),

    # path('payment/pay', views.PaymentView.as_view()),
    # path('payment/history', views.PaymentHistoryView.as_view()),
]