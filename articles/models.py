from django.db import models

# Create your models here.


class MongoTest(models.Model):
    name = models.CharField(max_length=100)
