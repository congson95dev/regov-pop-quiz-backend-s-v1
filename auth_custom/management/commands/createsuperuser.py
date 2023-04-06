from django.contrib.auth.management.commands.createsuperuser import Command as SuperUserCommand


class Command(SuperUserCommand):
    def handle(self, *args, **options):
        # i'm trying to override "python3 manage.py createsuperuser" command
        # the purpose is whenever super user created by that command,
        # i'll create record in table quiz_administrator as well.

        # edit 1:
        # i'm using alternative way, which is create admin by "fixtures" file
        # so we can ignore this way until we find a way to do this

        # edit 2:
        # i've found another way to do this
        # which is using signals to create admin whenever auth_user is created
        # please check in signals/signals.py
        a = 1
