from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
# pyrefly: ignore [missing-import]
from rest_framework import status
# pyrefly: ignore [missing-import]
from rest_framework.test import APITestCase
# pyrefly: ignore [missing-import]
from apps.users.models import UserProfile

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testgirl', password='password123')

    def test_profile_creation_signal_or_fallback(self):
        profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.assertEqual(profile.user.username, 'testgirl')
        self.assertEqual(profile.typical_cycle_length, 28)
        self.assertEqual(profile.typical_period_length, 5)


class AuthAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testgirl', password='password123', email='test@example.com')
        # pyrefly: ignore [missing-import]
        from rest_framework.authtoken.models import Token
        self.token = Token.objects.create(user=self.user)
        self.login_url = reverse('login')
        self.profile_url = reverse('user-profile')

    def test_login_success(self):
        data = {'username': 'testgirl', 'password': 'password123'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testgirl')

    def test_login_invalid_credentials(self):
        data = {'username': 'testgirl', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_retrieval_requires_auth(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_retrieval_and_update_with_auth(self):
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Get profile
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testgirl')

        # Update profile
        update_data = {
            'email': 'newtest@example.com',
            'profile': {
                'age': 25,
                'height': 165.50,
                'weight': 60.00,
                'fitness_level': 'Intermediate',
                'food_preferences': ['vegetarian']
            }
        }
        response = self.client.put(self.profile_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'newtest@example.com')
        self.assertEqual(response.data['profile']['age'], 25)
        self.assertEqual(response.data['profile']['fitness_level'], 'Intermediate')
