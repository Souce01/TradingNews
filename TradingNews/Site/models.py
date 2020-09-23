from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Company(models.Model):
    name    = models.CharField(max_length=50)
    symbol  = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    follow  = models.ManyToManyField(Company)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
