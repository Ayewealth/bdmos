from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView  # type: ignore

from .models import *
from .serializers import *
# Create your views here.


@api_view(['GET'])
def endpoints(request):
    data = [
        "signin/",
        "token/refresh/",
        "students/",
        "teachers/",
        "terms/",
        "sessions/",
        "subjects/",
        "class/",
        "events/",
        "notifications/",
        "school_photos/",
        "items/",
    ]
    return Response(data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserListCreateApiView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StudentListCreateApiView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        generated_username = serializer.data.get('username')
        generated_password = instance._generated_password

        print("Generated Username:", generated_username)
        print("Generated Password:", generated_password)

        return instance


class StudentRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'username'


class TeacherListCreateApiView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        generated_username = serializer.data.get('username')

        print("Generated Username:", generated_username)

        return instance
    


class TeacherRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'username'


class TermListCreateApiView(generics.ListCreateAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer


class SessionListCreateApiView(generics.ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class SubjectListCreateApiView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ClassListCreateApiView(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class EventListCreateApiView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class NotificationListCreateApiView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class SchoolPhotosListCreateApiView(generics.ListCreateAPIView):
    queryset = SchoolPhotos.objects.all()
    serializer_class = SchoolPhotosSerializer


class ItemsListCreateApiView(generics.ListCreateAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer


class ItemsRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    lookup_field = 'pk'


class SchemeListCreateApiView(generics.ListCreateAPIView):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer


class ResultListCreateApiView(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class SubjectResultListCreateApiView(generics.ListCreateAPIView):
    queryset = SubjectResult.objects.all()
    serializer_class = SubjectResultSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(data := kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)
