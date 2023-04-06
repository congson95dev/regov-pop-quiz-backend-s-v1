from django.core.management import BaseCommand, call_command
from django.contrib.auth import get_user_model

from quiz.models import Administrator

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        # it will call the command "python3 manage.py loaddata default_admin_info.json"
        call_command('loaddata', 'default_admin_info.json')
        user = User.objects.last()
        if user:
            # create quiz_administrator based on the created admin
            admin = Administrator.objects.create(user=user)
