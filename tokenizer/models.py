from django.conf import settings
from django.db import models


# Create your models here.

class Tokenoutput(models.Model):
    textoutput = models.TextField

    def __str__(self):
        return self.textoutput
