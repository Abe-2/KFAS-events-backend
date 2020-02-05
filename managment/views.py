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

from .models import Event, Attendee, Feedback
import managment.permissions as permissions
import managment.serializers as serializers


# TODO: should be descending
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
    permission_classes = [IsAuthenticated, permissions.IsEventCreatorFromAttendee]

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
        send_confirmation_email(attendee.id, attendee.email)


@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
def CheckinAttendee(request, attendee_id):
    attendee = Attendee.objects.filter(pk=attendee_id).values('event')
    print(attendee)
    content = {'status': 'ok'}

    event = Event.objects.get(pk=attendee[0]['event'])
    print(event)
    if event.created_by == request.user:
        Attendee.objects.filter(pk=attendee_id).update(did_attend=True)
    else:
        content = {'status': 'error'}

    return Response(content)


# @api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
# def EventMarkDone(request, event_id):
#     Event.objects.filter(pk=event_id).update(is_finished=True)
#
#     event = Event.objects.get(pk=event_id)
#     for attendee in Attendee.objects.filter(event_id=event_id, did_attend=True):
#         feedback = Feedback.objects.create(attendee=attendee.id, event=event.id)
#         send_feedback_email(event.name, attendee.email, feedback.id)
#
#     content = {'status': 'ok'}
#     return Response(content)


class EventMarkDone(UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventNoFields
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'

    permission_classes = [IsAuthenticated, permissions.IsEventCreator]

    def perform_update(self, serializer):
        serializer.save(is_finished=True)


class UserRegister(CreateAPIView):
    serializer_class = serializers.OrganizerRegister


class FeedbackList(ListAPIView):
    queryset = Feedback.objects.all()  # or .filter
    serializer_class = serializers.SubmitFeedback
    lookup_field = 'event'
    lookup_url_kwarg = 'event_id'


class SubmitFeedback(UpdateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = serializers.SubmitFeedback
    lookup_field = 'event'
    lookup_url_kwarg = 'feedback_id'


def send_confirmation_email(user_id, email):
    subject = 'Subject'
    html_message = render_to_string('mail_template.html', {'id': user_id})
    plain_message = strip_tags(html_message)
    # from_email = 'kfas-2@outlook.com'
    from_email = 'kfas1111111@gmail.com'
    to = email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


@api_view(['GET'])
def testemail(request):
    subject = 'Subject'
    html_message = render_to_string('mail_template.html', {'id': "7838"})
    plain_message = strip_tags(html_message)
    # from_email = 'kfas-2@outlook.com'
    from_email = 'kfas1111111@gmail.com'
    to = 'kfas-1@outlook.com'

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    content = {'status': 'ok'}
    return Response(content)
