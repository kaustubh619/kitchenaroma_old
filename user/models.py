from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
import random

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.BigIntegerField(default=7002821881)
    verfication_code = models.IntegerField(blank=True, null=True)
    user_location_latitude = models.FloatField(blank=True, null=True)
    user_location_longitude = models.FloatField(blank=True, null=True)
    gmap_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.email}'

# def pre_save_post_receiver_user(sender, instance, *args, **kwargs):
#     instance.verfication_code = random.randint(1111,9999)

# pre_save.connect(pre_save_post_receiver_user, sender=CustomUser)        
