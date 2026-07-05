from django.urls import path, include
from rest_framework.routers import SimpleRouter
# pyrefly: ignore [missing-import]
from apps.users.views import (
    LoginView, LogoutView, UserProfileView,
    SuperUserLoginView, SuperUserUserViewSet, SuperUserAppFeatureViewSet,
    AppFeatureListView
)

# pyrefly: ignore [missing-import]
from apps.content.views import SuperUserMealPlanViewSet, SuperUserRoutineViewSet

router = SimpleRouter()
router.register('superuser/users', SuperUserUserViewSet, basename='superuser-users')
router.register('superuser/features', SuperUserAppFeatureViewSet, basename='superuser-features')
router.register('superuser/meals', SuperUserMealPlanViewSet, basename='superuser-meals')
router.register('superuser/routines', SuperUserRoutineViewSet, basename='superuser-routines')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('superuser/login/', SuperUserLoginView.as_view(), name='superuser-login'),
    path('features/', AppFeatureListView.as_view(), name='features-list'),
    path('', include(router.urls)),
]

