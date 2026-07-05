# pyrefly: ignore [missing-import]
from rest_framework import serializers
# pyrefly: ignore [missing-import]
from apps.wellness.models import DailyHabitLog, SymptomLog, CycleLog

class DailyHabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyHabitLog
        fields = [
            'id', 'date', 'water_intake_ml', 'water_goal_ml', 
            'sleep_hours', 'exercise_completed', 'yoga_completed', 
            'meditation_completed', 'mood', 'weight', 'notes'
        ]
        read_only_fields = ['id']


class SymptomLogSerializer(serializers.ModelSerializer):
    symptom_display = serializers.CharField(source='get_symptom_name_display', read_only=True)
    
    class Meta:
        model = SymptomLog
        fields = ['id', 'date', 'symptom_name', 'symptom_display', 'severity', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class CycleLogSerializer(serializers.ModelSerializer):
    flow_display = serializers.CharField(source='get_flow_level_display', read_only=True)
    duration_days = serializers.SerializerMethodField()

    class Meta:
        model = CycleLog
        fields = ['id', 'start_date', 'end_date', 'flow_level', 'flow_display', 'notes', 'duration_days', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_duration_days(self, obj):
        if obj.end_date:
            return (obj.end_date - obj.start_date).days + 1
        return None
