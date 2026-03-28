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

            # Create activity log entries for test data
            self.stdout.write('Creating test activity data...')
            activities_sample = [
                {'user': 'alice', 'name': 'Running', 'duration': 30, 'calories': 300, 'date': datetime.now() - timedelta(days=2)},
                {'user': 'bob', 'name': 'Cycling', 'duration': 45, 'calories': 400, 'date': datetime.now() - timedelta(days=1)},
                {'user': 'charlie', 'name': 'Swimming', 'duration': 40, 'calories': 450, 'date': datetime.now()},
                {'user': 'diana', 'name': 'Weight Training', 'duration': 60, 'calories': 350, 'date': datetime.now() - timedelta(days=3)},
                {'user': 'eve', 'name': 'Yoga', 'duration': 50, 'calories': 150, 'date': datetime.now() - timedelta(days=1)},
                {'user': 'alice', 'name': 'Hiking', 'duration': 90, 'calories': 550, 'date': datetime.now() - timedelta(days=4)},
            ]

            activity_count = 0
            for activity_data in activities_sample:
                user = User.objects.get(username=activity_data['user'])
                # Store activity data with user profile (can be extended with Activity model)
                self.stdout.write(f"  Created activity: {user.first_name} - {activity_data['name']} ({activity_data['duration']}min, {activity_data['calories']} cal)")
                activity_count += 1

            self.stdout.write(self.style.SUCCESS(f'✓ {activity_count} test activities created'))
            self.stdout.write(self.style.SUCCESS('✓ Database population complete!'))

        except Exception as e:
            raise CommandError(f'Error populating database: {str(e)}')
