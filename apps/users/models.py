from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    FITNESS_LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField(null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    
    # Food preferences and allergies
    food_preferences = models.JSONField(default=list, blank=True, help_text="List of dietary preferences (e.g. Vegetarian, Keto)")
    allergies = models.TextField(blank=True, help_text="Comma-separated or list of allergies")
    
    # Fitness & Goals
    fitness_level = models.CharField(max_length=20, choices=FITNESS_LEVEL_CHOICES, default='Beginner')
    goals = models.TextField(blank=True, help_text="Wellness goals for managing PCOS")
    
    # Cycle Tracking Defaults
    typical_cycle_length = models.IntegerField(default=28, help_text="Average cycle length in days")
    typical_period_length = models.IntegerField(default=5, help_text="Average period length in days")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class AppFeature(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    is_enabled = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code}) - Enabled: {self.is_enabled}"

