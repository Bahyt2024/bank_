from rest_framework import serializers
from .models import Account, Credit, Transaction, Report

# Account Serializer
class AccountSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # добавляем user с read_only=True

    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'user')  # user добавляем в read_only_fields

# Credit Serializer
class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

# Transaction Serializer
class TransactionSerializer(serializers.Serializer):
    sender_card_number = serializers.CharField(max_length=16)
    receiver_card_number = serializers.CharField(max_length=16)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, data):
        try:
            sender_account = Account.objects.get(card_number=data['sender_card_number'])
        except Account.DoesNotExist:
            raise serializers.ValidationError("Отправитель с такой картой не найден")

        try:
            receiver_account = Account.objects.get(card_number=data['receiver_card_number'])
        except Account.DoesNotExist:
            raise serializers.ValidationError("Получатель с такой картой не найден")

        if sender_account == receiver_account:
            raise serializers.ValidationError("Нельзя отправить самому себе")

        if sender_account.balance < data['amount']:
            raise serializers.ValidationError("Недостаточно средств")

        data['sender_account'] = sender_account
        data['receiver_account'] = receiver_account
        return data

    def create(self, validated_data):
        sender_account = validated_data['sender_account']
        receiver_account = validated_data['receiver_account']
        amount = validated_data['amount']

        sender_account.balance -= amount
        receiver_account.balance += amount
        sender_account.save()
        receiver_account.save()

        transaction = Transaction.objects.create(
            sender_account=sender_account,
            receiver_account=receiver_account,
            amount=amount,
            status='completed'
        )

        return transaction

# Report Serializer
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('report_date',)
