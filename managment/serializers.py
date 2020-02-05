from rest_framework import serializers
from django.contrib.auth.models import User

from managment.models import Event, Attendee, Feedback


class OrganizerInfo(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class EventList(serializers.ModelSerializer):
    created_by = OrganizerInfo()

    class Meta:
        model = Event
        fields = '__all__'

    # def get_created_by(self, event):
    #     # author.book_set.all() # does same work as Book.objects.filter(author=author)
    #     print(event)
    #     return OrganizerInfo(User.objects.get(id=event.created_by)).data


class EventCreate(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['created_by', 'is_finished']


class EventNoFields(serializers.ModelSerializer):
    # is_finished = serializers.HiddenField(default=True)
    class Meta:
        model = Event
        fields = []

    # def validate(self, data):
    #     print("hello")
    #     for key in data.keys():
    #         print(key)
    #     print("hello")
    #     if not data['is_finished']:
    #         raise serializers.ValidationError("the event is already done")
    #     return data


class EventAttendees(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        exclude = ['event']


class SubmitFeedback(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']


class AttendeeRegister(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        exclude = ['event', 'did_attend']


class AttendeeInfo(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'


class CheckIn(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['did_attend']


class OrganizerRegister(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['password', 'username', 'email']

    def create(self, validated_data):
        password = validated_data['password']
        username = validated_data['username']
        email = validated_data['email']

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        return validated_data
