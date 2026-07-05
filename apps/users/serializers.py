# pyrefly: ignore [missing-import]
from rest_framework import serializers
from django.contrib.auth.models import User
# pyrefly: ignore [missing-import]
from apps.users.models import UserProfile, AppFeature

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'age', 'height', 'weight', 'food_preferences', 
            'allergies', 'fitness_level', 'goals', 
            'typical_cycle_length', 'typical_period_length',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # Update user fields
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update profile fields
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
            
        return instance


class AppFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppFeature
        fields = ['id', 'name', 'code', 'is_enabled', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class SuperUserUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_superuser', 'date_joined', 'profile']
        read_only_fields = ['date_joined']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password', None)
        
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
            
        UserProfile.objects.create(user=user, **(profile_data or {}))
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password', None)

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if 'is_superuser' in validated_data:
            instance.is_superuser = validated_data.get('is_superuser')
            instance.is_staff = validated_data.get('is_superuser')  # sync staff flag

        if password:
            instance.set_password(password)
            
        instance.save()

        if profile_data is not None:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance

