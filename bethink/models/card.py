from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Card(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    notification_date = models.DateTimeField(null=True)

    def get_absolute_url(self):
        return reverse('bethink:card', kwargs={'pk': self.pk})

    def __str__(self):
        return '"{title}" by {username}'.format(title=self.title,
                                                username=self.user.username)
