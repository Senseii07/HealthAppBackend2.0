from django.urls import path, include
# pyrefly: ignore [missing-import]
from rest_framework.routers import DefaultRouter
# pyrefly: ignore [missing-import]
from apps.content.views import MealPlanViewSet, RoutineViewSet, ResourceViewSet, DailyQuoteViewSet

router = DefaultRouter()
router.register(r'meals', MealPlanViewSet, basename='meal')
router.register(r'routines', RoutineViewSet, basename='routine')
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'quotes', DailyQuoteViewSet, basename='quote')

urlpatterns = [
    path('', include(router.urls)),
]
