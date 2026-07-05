# pyrefly: ignore [missing-import]
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
# pyrefly: ignore [missing-import]
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# pyrefly: ignore [missing-import]
from apps.users.models import UserProfile, AppFeature
# pyrefly: ignore [missing-import]
from apps.users.serializers import UserSerializer, UserProfileSerializer, AppFeatureSerializer, SuperUserUserSerializer

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Both username and password are required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response(
                {'error': 'Invalid credentials.'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        token, created = Token.objects.get_or_create(user=user)
        
        # Check if user has a profile
        has_profile = UserProfile.objects.filter(user=user).exists()
        
        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'has_profile': has_profile,
            'is_superuser': user.is_superuser
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Token not found.'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Ensure profile exists
        profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuperUserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Both username and password are required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response(
                {'error': 'Invalid credentials.'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        if not user.is_superuser:
            return Response(
                {'error': 'Access denied. You do not have superuser privileges.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'is_superuser': True
        }, status=status.HTTP_200_OK)


class SuperUserUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    serializer_class = SuperUserUserSerializer
    queryset = User.objects.all().order_by('-date_joined')


class SuperUserAppFeatureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    serializer_class = AppFeatureSerializer
    queryset = AppFeature.objects.all().order_by('code')


def ensure_default_features():
    defaults = [
        {"code": "meals", "name": "Meals Plan", "description": "Tailored PCOS-friendly meals and recipes.", "is_enabled": True},
        {"code": "checklist", "name": "Checklist", "description": "Daily habit tracker (water, sleep, activities).", "is_enabled": True},
        {"code": "tracker", "name": "Cycle Tracker", "description": "Period tracking, logs, and forecasts.", "is_enabled": True},
        {"code": "chat", "name": "AI Insights", "description": "Gemini-powered AI assistant for insights.", "is_enabled": True},
    ]
    for item in defaults:
        AppFeature.objects.get_or_create(code=item["code"], defaults={
            "name": item["name"],
            "description": item["description"],
            "is_enabled": item["is_enabled"]
        })


class AppFeatureListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ensure_default_features()
        features = AppFeature.objects.all().order_by('code')
        serializer = AppFeatureSerializer(features, many=True)
        return Response(serializer.data)

