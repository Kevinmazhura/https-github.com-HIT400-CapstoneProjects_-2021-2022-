from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from datetime import date
from .models import Profile
from datetime import datetime
import random  
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
def randomnumber(N):
	minimum = pow(10, N-1)
	maximum = pow(10, N) - 1
	return random.randint(minimum, maximum)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            first_name = "",
            last_name ="",
            email = "",
            email_verify = "",
            date_of_birth = "",
            bio = "",
            avatar = "",
            city ="",
            district = "",
            country_of_residence = "",
            hobby = "",
            slug = slugify(instance.username),
            )
        profile.save()