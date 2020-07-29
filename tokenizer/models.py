from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class Tokenoutput(models.Model):
    textoutput = models.TextField

    def __str__(self):
        return self.textoutput


class Keywords(models.Model):

    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    session_id = models.CharField(max_length=100)
    session_index = models.IntegerField()
    text = models.TextField()
    words = models.TextField()
    words_selected = models.TextField()
    keywords = models.TextField(null=True)

    def __str__(self):
        return self.text