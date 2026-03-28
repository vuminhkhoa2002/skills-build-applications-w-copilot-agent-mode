from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from octofit_tracker.models import Activity, UserProfile, Team
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data for OctoFit Tracker'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        try:
            if options['clear']:
                self.stdout.write('Clearing existing data...')
                Activity.objects.all().delete()
                UserProfile.objects.all().delete()
                Team.objects.all().delete()
                User.objects.all().delete()
                self.stdout.write(self.style.SUCCESS('✓ Existing data cleared'))

            # Create sample users
            self.stdout.write('Creating sample users...')
            users_data = [
                {
                    'username': 'alice',
                    'email': 'alice@octofit.com',
                    'first_name': 'Alice',
                    'last_name': 'Johnson'
                },
                {
                    'username': 'bob',
                    'email': 'bob@octofit.com',
                    'first_name': 'Bob',
                    'last_name': 'Smith'
                },
                {
                    'username': 'charlie',
                    'email': 'charlie@octofit.com',
                    'first_name': 'Charlie',
                    'last_name': 'Brown'
                },
                {
                    'username': 'diana',
                    'email': 'diana@octofit.com',
                    'first_name': 'Diana',
                    'last_name': 'Prince'
                },
                {
                    'username': 'eve',
                    'email': 'eve@octofit.com',
                    'first_name': 'Eve',
                    'last_name': 'Wilson'
                },
            ]

            created_users = []
            for user_data in users_data:
                user, created = User.objects.get_or_create(
                    username=user_data['username'],
                    defaults={
                        'email': user_data['email'],
                        'first_name': user_data['first_name'],
                        'last_name': user_data['last_name'],
                    }
                )
                if created:
                    user.set_password('octofit123')
                    user.save()
                    created_users.append(user)
                    self.stdout.write(f'  Created user: {user.username}')
                else:
                    self.stdout.write(f'  User already exists: {user.username}')

            self.stdout.write(self.style.SUCCESS(f'✓ {len(created_users)} sample users created/verified'))

            # Create user profiles
            self.stdout.write('Creating user profiles...')
            users = User.objects.all()
            for user in users:
                profile, created = UserProfile.objects.get_or_create(user=user)
                if created:
                    self.stdout.write(f'  Created profile for: {user.username}')

            # Create test activity data and save to database
            self.stdout.write('Creating test activity data...')
            # Use a fixed base date to ensure consistent lookups across runs
            base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            activities_sample = [
                {'user': 'alice', 'type': 'running', 'duration': 30, 'calories': 300, 'date': base_date - timedelta(days=2)},
                {'user': 'bob', 'type': 'cycling', 'duration': 45, 'calories': 400, 'date': base_date - timedelta(days=1)},
                {'user': 'charlie', 'type': 'swimming', 'duration': 40, 'calories': 450, 'date': base_date},
                {'user': 'diana', 'type': 'weight_training', 'duration': 60, 'calories': 350, 'date': base_date - timedelta(days=3)},
                {'user': 'eve', 'type': 'yoga', 'duration': 50, 'calories': 150, 'date': base_date - timedelta(days=1)},
                {'user': 'alice', 'type': 'hiking', 'duration': 90, 'calories': 550, 'date': base_date - timedelta(days=4)},
            ]

            # Clear previous test activities to ensure exactly 6 exist
            Activity.objects.filter(activity_type__in=['running', 'cycling', 'swimming', 'weight_training', 'yoga', 'hiking']).delete()
            
            activity_count = 0
            for activity_data in activities_sample:
                user = User.objects.get(username=activity_data['user'])
                activity = Activity(
                    user=user,
                    activity_type=activity_data['type'],
                    activity_date=activity_data['date'],
                    duration=activity_data['duration'],
                    calories_burned=activity_data['calories'],
                )
                activity.save()
                activity_count += 1
                activity_type_display = activity.get_activity_type_display()
                self.stdout.write(f"  Created activity: {user.first_name} - {activity_type_display} ({activity.duration}min, {activity.calories_burned} cal)")

            self.stdout.write(self.style.SUCCESS(f'✓ {activity_count} test activities created and saved'))

            # Verify activities were saved to database
            total_activities = Activity.objects.count()
            self.stdout.write(f'  Database verification: {total_activities} total activities in database')
            if total_activities < 6:
                self.stdout.write(self.style.WARNING(f'  Warning: Expected 6 activities, found {total_activities}'))

            # Create sample team
            self.stdout.write('Creating sample team...')
            team, created = Team.objects.get_or_create(
                name='Fitness Enthusiasts',
                defaults={
                    'description': 'A team of dedicated fitness trackers',
                    'created_by': User.objects.first(),
                }
            )
            if created:
                team.members.add(*users)
                self.stdout.write(f'  Created team: {team.name}')
            else:
                self.stdout.write(f'  Team already exists: {team.name}')

            self.stdout.write(self.style.SUCCESS('✓ Database population complete!'))

        except Exception as e:
            raise CommandError(f'Error populating database: {str(e)}')
