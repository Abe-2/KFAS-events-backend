"""events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from managment.views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('event/', EventList.as_view()),
    path('event/attendees/<int:event_id>', EventAttendees.as_view()),
    path('event/attendees/checkin/<int:attendee_id>', CheckinAttendee),
    path('event/create', EventCreate.as_view()),
    path('event/done/<int:event_id>', EventMarkDone.as_view()),
    path('event/register/<int:event_id>', EventRegister.as_view()),

    path('feedback/<int:event_id>', FeedbackList.as_view()),
    path('feedback/submit/<int:feedback_id>', SubmitFeedback.as_view()),

    # path('test/sendform', testemail),

    path('register', UserRegister.as_view()),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # TODO: make login with email instead of name
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
