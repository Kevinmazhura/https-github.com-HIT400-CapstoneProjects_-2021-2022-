from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from datetime import date
from .models import UserRegistrationModel
from datetime import datetime
import random  
from django.core.exceptions import ObjectDoesNotExist
# def randomnumber(N):
# 	minimum = pow(10, N-1)
# 	maximum = pow(10, N) - 1
# 	return random.randint(minimum, maximum)

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         profile = UserRegistrationModel.objects.create(user=instance)
#         profile.save()