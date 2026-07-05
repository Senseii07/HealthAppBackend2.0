# pyrefly: ignore [missing-import]
from rest_framework import serializers
# pyrefly: ignore [missing-import]
from apps.content.models import MealPlan, Routine, Resource, DailyQuote

class MealPlanSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = MealPlan
        fields = [
            'id', 'week_number', 'day_of_week', 'day_name', 
            'meal_type', 'name', 'description', 'recipe_link', 
            'calories', 'carbs_g', 'protein_g', 'fat_g', 
            'ingredients', 'is_pcos_friendly'
        ]


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = [
            'id', 'category', 'title', 'subtitle', 'difficulty', 
            'duration_minutes', 'description', 'steps', 
            'video_url', 'image_url', 'is_active'
        ]


class ResourceSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Resource
        fields = [
            'id', 'category', 'category_display', 'title', 
            'summary', 'content', 'source_name', 'source_url', 
            'published_date', 'image_url'
        ]


class DailyQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyQuote
        fields = ['id', 'quote', 'author']
