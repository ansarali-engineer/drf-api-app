from django.test import TestCase
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.test import APIClient

from Role.models import Role
from branch.models import Branch
from .models import User, UserToken
from .serializer import LoginSerializer


class LoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.role = Role.objects.create(name='Sales')
        self.branch = Branch.objects.create(name='Main', code='MAIN')
        self.user = User.objects.create(
            username='registered',
            role=self.role,
            branch=self.branch,
            email='registered@example.com',
            password=make_password('correct-password'),
            phone='123456789',
            first_name='Registered',
            last_name='User',
        )
    def test_registration_hashes_password(self):
        response = self.client.post('/api/users/', {
                'username': 'new-user',
                'role': self.role.pk,
                'branch': self.branch.pk,
                'email': 'new@example.com',
                'password': 'new-password',
                'phone': '123456789',
                'first_name': 'New',
                'last_name': 'User',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertNotIn('password', response.data)
        user = User.objects.get(username='new-user')
        self.assertNotEqual(user.password, 'new-password')
        self.assertTrue(check_password('new-password', user.password))
        self.assertTrue(user.is_active)
        login_serializer = LoginSerializer(data={
            'username': 'new-user',
            'password': 'new-password',
        })
        self.assertTrue(login_serializer.is_valid(), login_serializer.errors)

        login_response = self.client.post(
            '/api/login/',
            {'username': 'new-user', 'password': 'new-password'},
            format='json',
        )
        self.assertEqual(login_response.status_code, 200, login_response.data)
        self.assertEqual(set(login_response.data), {'access', 'refresh'})

    def test_login_returns_jwt_pair_for_custom_user(self):
        response = self.client.post(
            '/api/login/',
            {'username': 'registered', 'password': 'correct-password'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data), {'access', 'refresh'})
        self.assertTrue(response.data['access'])
        self.assertTrue(response.data['refresh'])

    def test_login_rejects_incorrect_password(self):
        response = self.client.post(
            '/api/login/',
            {'username': 'registered', 'password': 'wrong-password'},
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_token_endpoint_issues_refreshable_jwt(self):
        response = self.client.post(
            '/api/token/',
            {'username': 'registered', 'password': 'correct-password'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        refresh_response = self.client.post(
            '/api/token/refresh/',
            {'refresh': response.data['refresh']},
            format='json',
        )
        self.assertEqual(refresh_response.status_code, 200)
        self.assertTrue(refresh_response.data['access'])

    def test_token_authenticates_custom_user_on_protected_api(self):
        login_response = self.client.post(
            '/api/login/',
            {'username': 'registered', 'password': 'correct-password'},
            format='json',
        )

        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}"
        )
        response = client.get('/api/leadactivities/')

        self.assertEqual(response.status_code, 200)

    def test_legacy_token_login_remains_available(self):
        response = self.client.post(
            '/api/api-token-auth/',
            {'username': 'registered', 'password': 'correct-password'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['token'])
        self.assertTrue(UserToken.objects.filter(user=self.user).exists())
