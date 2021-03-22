from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, UserManager


class User(AbstractBaseUser):
    objects = UserManager()
    username = models.CharField(max_length=60,unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=60)
    phone = models.IntegerField()
    address = models.TextField()
    token= models.CharField(max_length=90)

    def __str__(self):
        return self.username


class BulkUser(models.Model):
    name = models.CharField(max_length=50,unique=True)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
