from rest_framework import serializers
from django.contrib.auth import authenticate

from api.models import Transaction, User


class TransactionSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=Transaction.TRANSACTION_TYPES)

    def validate_cache(self, user):
        if self.validated_data['type'] == Transaction.EXPENSE_TYPE:
            if user.cache < self.validated_data['amount']:
                raise serializers.ValidationError('You don\'t have enough cache!')

    class Meta:
        model = Transaction
        exclude = ('user',)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200, write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'],
            password=attrs['password']
        )

        if user:
            attrs['user'] = user

        return attrs

    def save(self, **kwargs):
        try:
            user = User.objects.create_user(
                username=self.validated_data['username'],
                password=self.validated_data['password']
            )
        except Exception as e:
            raise serializers.ValidationError(e.__str__())
        return user
