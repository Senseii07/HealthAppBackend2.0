import datetime
# pyrefly: ignore [missing-import]
from rest_framework import viewsets, status
# pyrefly: ignore [missing-import]
from rest_framework.decorators import action
# pyrefly: ignore [missing-import]
from rest_framework.response import Response
# pyrefly: ignore [missing-import]
from rest_framework.permissions import IsAuthenticated
# pyrefly: ignore [missing-import]
from apps.content.models import MealPlan, Routine, Resource, DailyQuote
# pyrefly: ignore [missing-import]
from apps.content.serializers import MealPlanSerializer, RoutineSerializer, ResourceSerializer, DailyQuoteSerializer

class MealPlanViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MealPlanSerializer
    permission_classes = [IsAuthenticated]
    queryset = MealPlan.objects.all()

    @action(detail=False, methods=['get'])
    def today(self, request):
        today_date = datetime.date.today()
        day_of_week = today_date.weekday()  # Monday is 0, Sunday is 6
        
        # Calculate rotating week based on the current ISO week of the year
        # Find the unique week numbers in the database
        weeks = list(MealPlan.objects.values_list('week_number', flat=True).distinct())
        if not weeks:
            return Response({
                'week_number': 1,
                'day_name': today_date.strftime('%A'),
                'meals': []
            }, status=status.HTTP_200_OK)
            
        weeks.sort()
        iso_week = today_date.isocalendar()[1]
        # Rotate through the available weeks
        week_idx = (iso_week - 1) % len(weeks)
        rotating_week = weeks[week_idx]

        # Get meals for today
        meals = MealPlan.objects.filter(week_number=rotating_week, day_of_week=day_of_week)
        serializer = self.get_serializer(meals, many=True)
        
        return Response({
            'week_number': rotating_week,
            'day_name': today_date.strftime('%A'),
            'meals': serializer.data
        })

    @action(detail=False, methods=['get'])
    def weekly_plan(self, request):
        # Return full plan for a specific week or default to current rotating week
        weeks = list(MealPlan.objects.values_list('week_number', flat=True).distinct())
        if not weeks:
            return Response({
                'week_number': 1,
                'meals': []
            }, status=status.HTTP_200_OK)
        weeks.sort()

        week_param = request.query_params.get('week')
        if week_param:
            try:
                target_week = int(week_param)
            except ValueError:
                return Response({'error': 'Invalid week parameter.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            today_date = datetime.date.today()
            iso_week = today_date.isocalendar()[1]
            week_idx = (iso_week - 1) % len(weeks)
            target_week = weeks[week_idx]

        meals = MealPlan.objects.filter(week_number=target_week)
        serializer = self.get_serializer(meals, many=True)
        return Response({
            'week_number': target_week,
            'meals': serializer.data
        })


class RoutineViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RoutineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Routine.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Resource.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset


# pyrefly: ignore [missing-import]
from apps.users.views import IsSuperUser

class DailyQuoteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DailyQuoteSerializer
    permission_classes = [IsAuthenticated]
    queryset = DailyQuote.objects.all()

    @action(detail=False, methods=['get'])
    def today(self, request):
        quotes = list(DailyQuote.objects.all())
        if not quotes:
            return Response({
                'quote': 'Keep shining, beautiful soul. You are doing amazing.',
                'author': 'PCOS Companion'
            })
            
        today_val = datetime.date.today()
        day_of_year = today_val.timetuple().tm_yday
        quote_idx = day_of_year % len(quotes)
        selected_quote = quotes[quote_idx]
        
        serializer = self.get_serializer(selected_quote)
        return Response(serializer.data)


class SuperUserMealPlanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    serializer_class = MealPlanSerializer
    queryset = MealPlan.objects.all().order_by('week_number', 'day_of_week', 'meal_type')


class SuperUserRoutineViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    serializer_class = RoutineSerializer
    queryset = Routine.objects.all().order_by('category', 'title')

