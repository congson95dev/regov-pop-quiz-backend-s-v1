from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from quiz.models import Administrator


# use signals to create admin whenever an auth_user is created.
@receiver(post_save, sender=User)
def save_admin_user_for_super_user(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        admin = Administrator.objects.create(user=instance)
        admin.save()
