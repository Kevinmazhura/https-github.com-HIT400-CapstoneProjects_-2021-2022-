"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

from hardreco.settings import MEDIA_ROOT
from shop.models import Category

Image_default = MEDIA_ROOT + 'frame.png'
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'store/{1}'.format(instance.name, filename)

def product_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return '{0}/{1}/{2}'.format(instance.store.name,instance.name, filename)

#class MyModel(models.Model):
#    upload = models.ImageField(upload_to = user_directory_path)
# Create your models here.
class OnlineStore(models.Model):
    image = models.ImageField(null=True,upload_to =user_directory_path)
    name = models.CharField(null=False ,max_length=100)
    phone = models.IntegerField(null=False,default=0)    
    city = models.CharField(null=False,max_length=100)    
    website = models.CharField(null=False ,max_length=100)
    address = models.TextField(null=False ,max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=1)
    def __str__(self):
        return self.name

class Product(models.Model):
    image = models.ImageField(null=True,upload_to =product_directory_path,default=Image_default)
    name = models.CharField(null=False ,max_length=1000)
    online_image_url = models.CharField(null=True ,max_length=1000)
    store = models.ForeignKey(OnlineStore, on_delete=models.CASCADE)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    description = models.TextField(null=False ,max_length=1000)
    price = models.CharField(null=False,max_length=100)
    link = models.CharField(null=True,max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=1)
    def __str__(self):
        return self.name

class StoreCategory(models.Model):
    name = models.CharField(null=False,max_length=500)
    image = models.CharField(null=True,max_length=1000)
    link = models.CharField(null=True,max_length=1000)
    status = models.BooleanField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Person(models.Model):
    sys_user = models.OneToOneField(User, on_delete=models.CASCADE)
    person_code = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)
    date_of_joining = models.DateField(null=True)
    address = models.TextField(null=True)
    def __str__(self):
        return self.person_code

class PersonProfile(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.person}' 
    class Meta:
        abstract = True

class Customer(PersonProfile):
    customer_code = models.IntegerField()

class Seller(PersonProfile):
    store_name= models.CharField(max_length=255)    
    store_code = models.IntegerField()