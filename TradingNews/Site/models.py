from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Company(models.Model):
    name    = models.CharField(max_length=50)
    link    = models.CharField(max_length=200, null=True)
    symbol  = models.CharField(max_length=20, null=True)
    logo    = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title   = models.CharField(max_length=50)
    link    = models.CharField(max_length=200, null=True)
    date    = models.DateTimeField()
    network = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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
