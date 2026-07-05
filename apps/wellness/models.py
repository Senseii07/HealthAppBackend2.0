from django.db import models
from django.contrib.auth.models import User

class DailyHabitLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habit_logs')
    date = models.DateField()
    
    # Hydration
    water_intake_ml = models.IntegerField(default=0, help_text="Total water consumed in ml")
    water_goal_ml = models.IntegerField(default=2000, help_text="Target water goal in ml")
    
    # Sleep
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Hours of sleep")
    
    # Habits
    exercise_completed = models.BooleanField(default=False)
    yoga_completed = models.BooleanField(default=False)
    meditation_completed = models.BooleanField(default=False)
    
    # Well-being markers
    mood = models.IntegerField(null=True, blank=True, help_text="Mood rating from 1 (poor) to 5 (excellent)")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight logged in kg")
    notes = models.TextField(blank=True, help_text="General comments or observations")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='unique_user_daily_log')
        ]

    def __str__(self):
        return f"{self.user.username}'s log for {self.date}"


class SymptomLog(models.Model):
    SYMPTOM_CHOICES = [
        ('Cramps', 'Cramps'),
        ('Bloating', 'Bloating'),
        ('Acne', 'Acne'),
        ('Fatigue', 'Fatigue'),
        ('Headache', 'Headache'),
        ('Mood Swings', 'Mood Swings'),
        ('Insomnia', 'Insomnia'),
        ('Cravings', 'Cravings'),
        ('Backache', 'Backache'),
        ('Nausea', 'Nausea'),
    ]
    
    SEVERITY_CHOICES = [
        ('Mild', 'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='symptom_logs')
    date = models.DateField()
    symptom_name = models.CharField(max_length=50, choices=SYMPTOM_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='Mild')
    notes = models.TextField(blank=True, help_text="Specific symptom comments")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'symptom_name']

    def __str__(self):
        return f"{self.user.username} - {self.symptom_name} ({self.severity}) on {self.date}"


class CycleLog(models.Model):
    FLOW_CHOICES = [
        ('Spotting', 'Spotting'),
        ('Light', 'Light'),
        ('Medium', 'Medium'),
        ('Heavy', 'Heavy'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cycle_logs')
    start_date = models.DateField(help_text="Start date of period")
    end_date = models.DateField(null=True, blank=True, help_text="End date of period (leave blank if current/ongoing)")
    flow_level = models.CharField(max_length=20, choices=FLOW_CHOICES, default='Medium')
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        end_str = self.end_date.strftime('%Y-%m-%d') if self.end_date else 'Ongoing'
        return f"{self.user.username}'s Period: {self.start_date} to {end_str}"
