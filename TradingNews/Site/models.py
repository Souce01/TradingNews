from django.db import models
from django.contrib.auth.models import User

# model is used to keep track of which user follows which stocks
class Follows(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol  = models.CharField(max_length=5)
    name    = models.CharField(max_length=50, default='null')

    def __str__(self):
        return f'{self.user.username} - {self.symbol}'

    @staticmethod
    def get_user_follows_quote(user, alphaVantage):
        followedList = {}
        for follow in Follows.objects.filter(user=user):
            endPoint = alphaVantage.quote(symbol=follow.symbol)
            followedList.update({follow.symbol: endPoint})
        return followedList
