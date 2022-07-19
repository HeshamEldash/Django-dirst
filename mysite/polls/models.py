from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date Published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)
    special_number = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return self.user.username
