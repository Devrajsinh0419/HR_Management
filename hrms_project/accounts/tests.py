from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserRoleModelTests(TestCase):
    def test_create_superuser_sets_admin_role(self):
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='StrongPass123',
            first_name='Admin',
            last_name='User',
        )

        self.assertEqual(user.role, User.Roles.ADMIN)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_admin)


class AccountApiTests(APITestCase):
    def test_register_defaults_to_employee_role(self):
        payload = {
            'email': 'employee@example.com',
            'first_name': 'Regular',
            'last_name': 'Employee',
            'password': 'StrongPass123',
            'confirm_password': 'StrongPass123',
        }

        response = self.client.post(reverse('accounts-register'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['role'], User.Roles.EMPLOYEE)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_register_allows_hr_role(self):
        payload = {
            'email': 'hr@example.com',
            'first_name': 'HR',
            'last_name': 'Member',
            'password': 'StrongPass123',
            'confirm_password': 'StrongPass123',
            'role': User.Roles.HR,
        }

        response = self.client.post(reverse('accounts-register'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['role'], User.Roles.HR)

    def test_register_rejects_removed_manager_role(self):
        payload = {
            'email': 'manager@example.com',
            'first_name': 'Old',
            'last_name': 'Manager',
            'password': 'StrongPass123',
            'confirm_password': 'StrongPass123',
            'role': 'manager',
        }

        response = self.client.post(reverse('accounts-register'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('role', response.data)

    def test_login_returns_tokens_and_user_role(self):
        user = User.objects.create_user(
            email='login@example.com',
            password='StrongPass123',
            first_name='Login',
            last_name='User',
            role=User.Roles.EMPLOYEE,
        )

        payload = {
            'email': user.email,
            'password': 'StrongPass123',
        }
        response = self.client.post(reverse('accounts-login'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['role'], User.Roles.EMPLOYEE)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_me_requires_authentication(self):
        response = self.client.get(reverse('accounts-me'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_authenticated_user(self):
        user = User.objects.create_user(
            email='me@example.com',
            password='StrongPass123',
            first_name='Me',
            last_name='User',
            role=User.Roles.HR,
        )
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('accounts-me'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['role'], User.Roles.HR)
