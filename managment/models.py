from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=60)
    desc = models.TextField()
    location = models.CharField(max_length=20)
    date = models.DateField()
    fee = models.IntegerField()
    max_attendees = models.IntegerField()
    is_finished = models.BooleanField(default=False)
    created_by = models.ForeignKey(to=User, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Attendee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=60)
    phone = models.CharField(max_length=16)
    did_attend = models.BooleanField(default=False)
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Feedback(models.Model):
    rating = models.IntegerField(null=True)
    comment = models.TextField(null=True)
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(to=Attendee, on_delete=models.CASCADE)

    def __str__(self):
        return self.attendee + " > " + self.event
