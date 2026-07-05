import datetime
# pyrefly: ignore [missing-import]
from rest_framework import viewsets, status
# pyrefly: ignore [missing-import]
from rest_framework.views import APIView
# pyrefly: ignore [missing-import]
from rest_framework.decorators import action
# pyrefly: ignore [missing-import]
from rest_framework.response import Response
# pyrefly: ignore [missing-import]
from rest_framework.permissions import IsAuthenticated

# pyrefly: ignore [missing-import]
from apps.wellness.models import DailyHabitLog, SymptomLog, CycleLog
# pyrefly: ignore [missing-import]
from apps.wellness.serializers import DailyHabitLogSerializer, SymptomLogSerializer, CycleLogSerializer
# pyrefly: ignore [missing-import]
from apps.users.models import UserProfile

# Cross-app imports for dashboard consolidation
# pyrefly: ignore [missing-import]
from apps.content.models import MealPlan, Routine, DailyQuote
# pyrefly: ignore [missing-import]
from apps.content.serializers import MealPlanSerializer, RoutineSerializer

class DailyHabitLogViewSet(viewsets.ModelViewSet):
    serializer_class = DailyHabitLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailyHabitLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def by_date(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({'error': 'Date query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            date_val = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create an empty log for that date
        log, created = DailyHabitLog.objects.get_or_create(
            user=request.user,
            date=date_val,
            defaults={'water_intake_ml': 0, 'water_goal_ml': 2000}
        )
        serializer = self.get_serializer(log)
        return Response(serializer.data)


class SymptomLogViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SymptomLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CycleLogViewSet(viewsets.ModelViewSet):
    serializer_class = CycleLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CycleLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def predictions(self, request):
        user = request.user
        logs = list(CycleLog.objects.filter(user=user).order_by('start_date'))
        
        # Determine average cycle length
        cycle_lengths = []
        for i in range(1, len(logs)):
            diff = (logs[i].start_date - logs[i-1].start_date).days
            if 15 <= diff <= 60:
                cycle_lengths.append(diff)

        # Default values from profile
        try:
            profile = user.profile
            typical_cycle = profile.typical_cycle_length or 28
            typical_period = profile.typical_period_length or 5
        except UserProfile.DoesNotExist:
            typical_cycle = 28
            typical_period = 5

        avg_cycle_length = sum(cycle_lengths) / len(cycle_lengths) if cycle_lengths else typical_cycle
        
        # Predict next 3 periods
        predictions = []
        if logs:
            last_start = logs[-1].start_date
        else:
            last_start = datetime.date.today()

        current_prediction_start = last_start
        for _ in range(3):
            predicted_start = current_prediction_start + datetime.timedelta(days=int(avg_cycle_length))
            predicted_end = predicted_start + datetime.timedelta(days=typical_period - 1)
            
            predictions.append({
                'predicted_start_date': predicted_start.strftime('%Y-%m-%d'),
                'predicted_end_date': predicted_end.strftime('%Y-%m-%d'),
            })
            current_prediction_start = predicted_start

        return Response({
            'average_cycle_length': int(avg_cycle_length),
            'typical_period_length': typical_period,
            'predictions': predictions
        })


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = datetime.date.today()

        # 1. Get today's habit log
        habit_log, _ = DailyHabitLog.objects.get_or_create(
            user=user,
            date=today,
            defaults={'water_intake_ml': 0, 'water_goal_ml': 2000}
        )
        habit_data = DailyHabitLogSerializer(habit_log).data

        # 2. Get today's rotating meals
        weeks = list(MealPlan.objects.values_list('week_number', flat=True).distinct())
        meals_data = []
        rotating_week = 1
        if weeks:
            weeks.sort()
            iso_week = today.isocalendar()[1]
            week_idx = (iso_week - 1) % len(weeks)
            rotating_week = weeks[week_idx]
            meals = MealPlan.objects.filter(week_number=rotating_week, day_of_week=today.weekday())
            meals_data = MealPlanSerializer(meals, many=True).data

        # 3. Get daily quote
        quotes = list(DailyQuote.objects.all())
        quote_data = {
            'quote': 'Keep shining, beautiful soul. You are doing amazing.',
            'author': 'PCOS Companion'
        }
        if quotes:
            day_of_year = today.timetuple().tm_yday
            q = quotes[day_of_year % len(quotes)]
            quote_data = {'quote': q.quote, 'author': q.author}

        # 4. Get menstrual cycle overview
        active_period = CycleLog.objects.filter(user=user, end_date__isnull=True).order_by('-start_date').first()
        cycle_info = {
            'in_period': False,
            'period_day': None,
            'days_until_next': None
        }
        
        if active_period:
            cycle_info['in_period'] = True
            cycle_info['period_day'] = (today - active_period.start_date).days + 1
        else:
            logs = list(CycleLog.objects.filter(user=user).order_by('start_date'))
            try:
                profile = user.profile
                typical_cycle = profile.typical_cycle_length or 28
            except UserProfile.DoesNotExist:
                typical_cycle = 28
                
            cycle_lengths = []
            for i in range(1, len(logs)):
                diff = (logs[i].start_date - logs[i-1].start_date).days
                if 15 <= diff <= 60:
                    cycle_lengths.append(diff)
            
            avg_cycle_length = sum(cycle_lengths) / len(cycle_lengths) if cycle_lengths else typical_cycle
            
            if logs:
                last_start = logs[-1].start_date
                next_start = last_start + datetime.timedelta(days=int(avg_cycle_length))
                days_until = (next_start - today).days
                cycle_info['days_until_next'] = days_until if days_until >= 0 else 0
            else:
                cycle_info['days_until_next'] = None

        # 5. Get suggested routine based on day of the week
        weekday = today.weekday()
        category = 'Workout'
        if weekday in [0, 2, 4]:
            category = 'Yoga'
        elif weekday in [5, 6]:
            category = 'Meditation'
            
        routine = Routine.objects.filter(category=category, is_active=True).first()
        routine_data = RoutineSerializer(routine).data if routine else None

        # 6. Today's symptoms
        symptoms = SymptomLog.objects.filter(user=user, date=today)
        symptoms_data = SymptomLogSerializer(symptoms, many=True).data

        return Response({
            'date': today.strftime('%Y-%m-%d'),
            'day_name': today.strftime('%A'),
            'habits': habit_data,
            'meals': meals_data,
            'meals_week': rotating_week,
            'quote': quote_data,
            'cycle': cycle_info,
            'suggested_routine': routine_data,
            'today_symptoms': symptoms_data
        })
