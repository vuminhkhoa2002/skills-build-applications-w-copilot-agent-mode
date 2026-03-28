from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    """Model to track user activities and workouts"""
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('weight_training', 'Weight Training'),
        ('yoga', 'Yoga'),
        ('hiking', 'Hiking'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration = models.IntegerField(help_text='Duration in minutes')
    calories_burned = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    activity_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-activity_date']
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} ({self.duration}min)"


class Team(models.Model):
    """Model for team management"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name='teams')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Leaderboard(models.Model):
    """Model for team leaderboards"""
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='leaderboard')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Leaderboard for {self.team.name}"


class UserProfile(models.Model):
    """Extended user profile for fitness tracking"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    total_calories = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
