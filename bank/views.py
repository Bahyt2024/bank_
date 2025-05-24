# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Account, Credit, Transaction, Report
from .serializers import AccountSerializer, CreditSerializer, TransactionSerializer, ReportSerializer
from django.utils import timezone

# 🟢 Accounts
class CreateAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # user передаём явно
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_id):
        account = get_object_or_404(Account, id=account_id, user=request.user)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

class UpdateAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, account_id):
        account = get_object_or_404(Account, id=account_id, user=request.user)
        serializer = AccountSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllAccountsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

# 🟢 Credits
class CreateCreditView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetCreditView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, credit_id):
        credit = get_object_or_404(Credit, id=credit_id, user=request.user)
        serializer = CreditSerializer(credit)
        return Response(serializer.data)

class UpdateCreditView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, credit_id):
        credit = get_object_or_404(Credit, id=credit_id, user=request.user)
        serializer = CreditSerializer(credit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllCreditsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        credits = Credit.objects.filter(user=request.user)
        serializer = CreditSerializer(credits, many=True)
        return Response(serializer.data)

# 🟢 Transactions
class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()
            return Response({
                "message": "Перевод выполнен успешно",
                "transaction": {
                    "id": transaction.id,
                    "amount": str(transaction.amount),
                    "status": transaction.status,
                    "date": transaction.transaction_date
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetTransactionByIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id, sender=request.user)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

class GetTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(sender=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

class CancelTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        transaction = get_object_or_404(Transaction, id=id, sender=request.user, status='pending')
        transaction.status = 'cancelled'
        transaction.save()
        return Response({'message': 'Transaction cancelled'})

# 🟢 Reports
class TransactionsReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reports = Report.objects.filter(user=request.user, category='transactions')
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

class FinancialSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reports = Report.objects.filter(user=request.user)
        income = sum([r.totalIncome for r in reports])
        spending = sum([r.totalSpending for r in reports])
        return Response({
            'total_income': income,
            'total_spending': spending,
            'net': income - spending
        })
