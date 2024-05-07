from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.title