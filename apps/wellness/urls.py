from django.urls import path, include
# pyrefly: ignore [missing-import]
from rest_framework.routers import DefaultRouter
# pyrefly: ignore [missing-import]
from apps.wellness.views import DailyHabitLogViewSet, SymptomLogViewSet, CycleLogViewSet, DashboardView

router = DefaultRouter()
router.register(r'habits', DailyHabitLogViewSet, basename='habit')
router.register(r'symptoms', SymptomLogViewSet, basename='symptom')
router.register(r'cycles', CycleLogViewSet, basename='cycle')

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', include(router.urls)),
]
