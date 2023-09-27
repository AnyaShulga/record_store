from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    address = models.TextField(max_length=500, blank=True)


@receiver(signal=post_save, sender=User)
def user_saved_handler(instance: User, created: bool, **kwargs):
    if not created:
        return

    Customer.objects.create(user=instance)

