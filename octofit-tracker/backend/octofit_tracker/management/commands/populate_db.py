from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
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
                self.stdout.write('Clearing existing users...')
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

            # Sample activities data
            activities_sample = [
                {'name': 'Running', 'duration': 30, 'calories': 300},
                {'name': 'Cycling', 'duration': 45, 'calories': 400},
                {'name': 'Swimming', 'duration': 40, 'calories': 450},
                {'name': 'Weight Training', 'duration': 60, 'calories': 350},
                {'name': 'Yoga', 'duration': 50, 'calories': 150},
                {'name': 'Hiking', 'duration': 90, 'calories': 550},
            ]

            self.stdout.write('Sample activities prepared:')
            for activity in activities_sample:
                self.stdout.write(f"  - {activity['name']}: {activity['duration']}min, {activity['calories']} cal")

            self.stdout.write(self.style.SUCCESS('✓ Database population complete!'))
            self.stdout.write('Ready to create more models: Team, Activity, Leaderboard, etc.')

        except Exception as e:
            raise CommandError(f'Error populating database: {str(e)}')
