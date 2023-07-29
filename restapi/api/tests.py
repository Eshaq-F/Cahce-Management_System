from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from api.models import Transaction

User = get_user_model()


class APITest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create some test transactions
        Transaction.objects.create(user=self.user, amount=100, type=Transaction.INCOME_TYPE, category='Salary')
        Transaction.objects.create(user=self.user, amount=50, type=Transaction.EXPENSE_TYPE, category='Food')
        Transaction.objects.create(user=self.user, amount=200, type=Transaction.EXPENSE_TYPE, category='Rent')

        # Set up URLs for the views
        self.registration_url = reverse('user-login-register')
        self.logout_url = reverse('user-logout')
        self.transaction_list_create_url = reverse('list-create')
        self.transaction_detail_url = reverse('retrieve-update-delete', kwargs={'pk': self.user.transactions.first().pk})

    def test_user_registration(self):
        # Bad request: Missing password
        data = {'username': 'newuser'}
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Bad request: Invalid username/password combination
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Success
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_logout(self):
        # Bad request: Missing refresh token
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Success
        response = self.client.get(self.logout_url, HTTP_REFRESH_TOKEN='fake_refresh_token')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_transaction_list_create(self):
        # Bad request: Missing amount
        data = {'type': Transaction.INCOME_TYPE, 'category': 'Test'}
        response = self.client.post(self.transaction_list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Bad request: Insufficient cache for expense
        data = {'amount': 500, 'type': Transaction.EXPENSE_TYPE, 'category': 'Test Expense'}
        response = self.client.post(self.transaction_list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Success: Create new transaction
        data = {'amount': 50, 'type': Transaction.INCOME_TYPE, 'category': 'Test'}
        response = self.client.post(self.transaction_list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_transaction_retrieve_update_delete(self):
        # Bad request: Non-existent transaction ID
        response = self.client.get(reverse('transaction-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Success: Retrieve transaction
        response = self.client.get(self.transaction_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Success: Update transaction
        data = {'amount': 150, 'type': Transaction.INCOME_TYPE, 'category': 'Updated'}
        response = self.client.put(self.transaction_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Success: Delete transaction
        response = self.client.delete(self.transaction_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
