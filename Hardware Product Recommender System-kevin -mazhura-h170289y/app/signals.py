from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import *
from datetime import datetime
import random  

print("Singal Hello")

def randomnumber(N):
	minimum = pow(10, N-1)
	maximum = pow(10, N) - 1
	return random.randint(minimum, maximum)

@receiver(post_save, sender=User)
def create_person(sender, instance, created, **kwargs):
    print("Singal Hello")
    if created:
        person = Person.objects.create(sys_user=instance)
        person.person_code = "ps" + str(randomnumber(10))
        person.date_of_birth = ""
        person.date_of_joining = datetime.now()
        person.address = ""
        person.save()
