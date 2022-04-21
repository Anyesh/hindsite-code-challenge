from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, User


@receiver(post_save, sender=User)
def create_or_update_superuser_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.update_or_create(user=instance)
        instance.profile.save()
