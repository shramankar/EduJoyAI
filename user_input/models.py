from django.db import models

# Create your models here.
from django.db import models


class UserResponse(models.Model):
    age = models.IntegerField()
    interests = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
