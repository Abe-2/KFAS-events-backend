from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, post_delete, post_init
from django.dispatch import receiver

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Event(models.Model):
    title = models.CharField(max_length=60)
    desc = models.TextField()
    location = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField(null=True)
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
        return self.attendee.first_name + " " + self.attendee.first_name + " > " + self.event.title


@receiver(pre_save, sender=Event)
def check_to_send_email(instance, *args, **kwargs):
    # print(kwargs)
    if instance.pk is not None:  # already exists
        old = Event.objects.get(pk=instance.pk)

        if old.is_finished is False and instance.is_finished is True:
            for attendee in Attendee.objects.filter(event_id=instance.id, did_attend=True):
                feedback = Feedback.objects.create(attendee_id=attendee.id, event_id=instance.id)
                send_feedback_email(instance.title, attendee.email, feedback.id)


def send_feedback_email(event_name, email, feedback_code):
    subject = 'Subject'
    html_message = render_to_string('form_email.html',
                                    {
                                        'event_name': event_name,
                                        'feedback_link': "https://zen-yalow-035b6d.netlify.com/feedback/" + str(feedback_code)
                                    })
    plain_message = strip_tags(html_message)
    # from_email = 'kfas-1@outlook.com'
    from_email = 'kfas1111111 @ gmail.com'
    to = email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
