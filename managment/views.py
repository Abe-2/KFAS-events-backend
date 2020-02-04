from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView, UpdateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Event, Attendee
import managment.serializers as serializers


class EventList(ListAPIView):
    queryset = Event.objects.all()  # or .filter
    serializer_class = serializers.EventList


class EventCreate(CreateAPIView):
    serializer_class = serializers.EventCreate
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(created_by=self.request.user)


# TODO: check that the user is the event creator
class EventAttendees(ListAPIView):
    serializer_class = serializers.EventAttendees
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = 'event_id'

    def get_queryset(self):
        event_id = self.kwargs.get(self.lookup_url_kwarg)
        return Attendee.objects.filter(event_id=event_id)


# TODO: decrement available seats
class EventRegister(CreateAPIView):
    serializer_class = serializers.AttendeeRegister

    lookup_url_kwarg = 'event_id'

    def perform_create(self, serializer):
        event_id = self.kwargs.get(self.lookup_url_kwarg)
        serializer.save(event_id=event_id)

        attendee = Attendee.objects.latest('id')
        send_email(attendee.id, attendee.email)


# TODO: check that the authenticated user is the creator of the attendee event
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def CheckinAttendee(request, attendee_id):
    Attendee.objects.filter(pk=attendee_id).update(did_attend=True)

    content = {
        'status': 'ok'
    }
    return Response(content)


class UserRegister(CreateAPIView):
    serializer_class = serializers.OrganizerRegister


def send_email(user_id, email):
    subject = 'Subject'
    html_message = render_to_string('mail_template.html', {'id': user_id})
    plain_message = strip_tags(html_message)
    from_email = 'kfas-1@outlook.com'
    to = email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    # send_mail(
    #     'Subject here',
    #     'Here is the message.',
    #     'kfas-1@outlook.com',
    #     ['agg2@outlook.com'],
    #     fail_silently=False,
    # )
    # return HttpResponse("This is a simple response !")
