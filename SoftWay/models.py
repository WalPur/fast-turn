from django.db import models
from django.contrib.auth.models import User

class comment(models.Model):
	author = models.CharField(max_length=255)
	text = models.TextField()
class queue(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()
	creator = models.CharField(max_length=255)
	people = models.TextField()
	openTime = models.PositiveSmallIntegerField()
	closeTime = models.PositiveSmallIntegerField()
	period = models.PositiveSmallIntegerField()
	last = models.TextField()
	time = models.TextField()
class people(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	queues = models.TextField()
	time = models.TextField()
class Test(models.Model):
	time = models.TimeField()
'''
class queuePosition(models.Model):
	name = models.CharField(max_length=255)
	time = models.TimeField()
'''