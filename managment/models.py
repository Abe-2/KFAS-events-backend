from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=60)
    desc = models.TextField()
    location = models.CharField(max_length=20)
    date = models.DateField()
    fee = models.IntegerField()
    max_attendees = models.IntegerField()
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


# class Event_Attendees(models.Model):
#     event = models.ForeignKey(to=Event, on_delete=models.CASCADE)
#     person = models.ForeignKey(to=Attendee, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.event + " > " + self.person
