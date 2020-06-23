from django.db import models
from django.conf import settings


# Create your models here.

class Tokenoutput(models.Model):
    textoutput = models.TextField

    def __str__(self):
        return self.textoutput
