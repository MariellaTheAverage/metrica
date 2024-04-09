from django.db import models
import time

class Metric(models.Model):
    int_timestamp = models.IntegerField(default=int(time.time()))
    int_value = models.IntegerField(default=0)

'''
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
'''