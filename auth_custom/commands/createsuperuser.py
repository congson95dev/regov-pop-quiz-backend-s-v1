from django.contrib.auth.management.commands.createsuperuser import Command as SuperUserCommand


class Command(SuperUserCommand):
    def handle(self, *args, **options):
        a = 1
