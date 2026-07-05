from django.db import models

class MealPlan(models.Model):
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    MEAL_TYPE_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    ]

    week_number = models.IntegerField(default=1, help_text="Meal plan week number for rotation (e.g. Week 1, Week 2)")
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    recipe_link = models.URLField(blank=True, null=True)
    
    # Nutrition facts
    calories = models.IntegerField(null=True, blank=True)
    carbs_g = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="Carbohydrates in grams")
    protein_g = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="Protein in grams")
    fat_g = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="Fat in grams")
    
    ingredients = models.JSONField(default=list, blank=True, help_text="List of ingredients needed")
    is_pcos_friendly = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['week_number', 'day_of_week', 'meal_type']
        constraints = [
            models.UniqueConstraint(fields=['week_number', 'day_of_week', 'meal_type'], name='unique_meal_plan_slot')
        ]

    def __str__(self):
        return f"Week {self.week_number} - {self.get_day_of_week_display()} - {self.meal_type}: {self.name}"


class Routine(models.Model):
    CATEGORY_CHOICES = [
        ('Workout', 'Workout'),
        ('Yoga', 'Yoga'),
        ('Meditation', 'Meditation'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, help_text="e.g. 15 mins • Beginner")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Beginner')
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    description = models.TextField()
    steps = models.JSONField(default=list, blank=True, help_text="Sequential steps/instructions")
    video_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'title']

    def __str__(self):
        return f"[{self.category}] {self.title} ({self.duration_minutes} mins)"


class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('Basics', 'PCOS Basics'),
        ('Nutrition', 'Nutrition & Diet'),
        ('Exercise', 'Exercise & Fitness'),
        ('Hormones', 'Hormones & Health'),
        ('Fertility', 'Fertility'),
        ('Stress', 'Stress Management'),
        ('News', 'Latest News'),
    ]

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255)
    summary = models.TextField(help_text="Short teaser description")
    content = models.TextField(help_text="Full markdown or rich text content")
    source_name = models.CharField(max_length=100, blank=True, help_text="For news articles, specify source name")
    source_url = models.URLField(blank=True, null=True, help_text="For news articles, link to original source")
    published_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"


class DailyQuote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=100, default='Unknown')
    
    def __str__(self):
        return f'"{self.quote}" - {self.author}'
