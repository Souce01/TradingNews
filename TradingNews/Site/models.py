from django.db import models
from django.contrib.auth.models import User

class Follows(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol  = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.user.username} - {self.symbol}'