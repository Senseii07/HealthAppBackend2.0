import datetime
from django.contrib.auth.models import User
from django.urls import reverse
# pyrefly: ignore [missing-import]
from rest_framework import status
# pyrefly: ignore [missing-import]
from rest_framework.test import APITestCase
# pyrefly: ignore [missing-import]
from apps.wellness.models import DailyHabitLog, CycleLog
# pyrefly: ignore [missing-import]
from apps.content.models import MealPlan, DailyQuote

class WellnessAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testgirl', password='password123', email='test@example.com')
        # pyrefly: ignore [missing-import]
        from rest_framework.authtoken.models import Token
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.habits_url = reverse('habit-list')
        self.cycles_url = reverse('cycle-list')
        self.dashboard_url = reverse('dashboard')

    def test_daily_habits_by_date(self):
        # Retrieve by date (should get or create)
        response = self.client.get(reverse('habit-by-date') + '?date=2026-07-05')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['date'], '2026-07-05')
        
        # Verify it was saved in DB
        self.assertTrue(DailyHabitLog.objects.filter(user=self.user, date='2026-07-05').exists())

    def test_cycle_log_creation(self):
        data = {
            'start_date': '2026-06-01',
            'end_date': '2026-06-05',
            'flow_level': 'Medium'
        }
        response = self.client.post(self.cycles_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['duration_days'], 5)

    def test_cycle_predictions(self):
        # Create two historical cycles (spaced by 28 days)
        CycleLog.objects.create(user=self.user, start_date='2026-04-01', end_date='2026-04-05')
        CycleLog.objects.create(user=self.user, start_date='2026-04-29', end_date='2026-05-03')
        
        response = self.client.get(reverse('cycle-predictions'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_cycle_length'], 28)
        self.assertEqual(len(response.data['predictions']), 3)
        
        # Next start should be 2026-04-29 + 28 days = 2026-05-27
        self.assertEqual(response.data['predictions'][0]['predicted_start_date'], '2026-05-27')

    def test_dashboard_aggregation(self):
        # Seed a meal and quote to avoid empty responses
        MealPlan.objects.create(week_number=1, day_of_week=datetime.date.today().weekday(), meal_type='Breakfast', name='Oatmeal')
        DailyQuote.objects.create(quote='You got this!', author='Companion')
        
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('habits', response.data)
        self.assertIn('meals', response.data)
        self.assertIn('quote', response.data)
        self.assertIn('cycle', response.data)
        self.assertEqual(response.data['quote']['quote'], 'You got this!')
