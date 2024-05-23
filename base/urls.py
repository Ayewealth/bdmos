from django.urls import path
from rest_framework_simplejwt.views import (  # type: ignore
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path("", views.endpoints, name="endpoints"),

    # Auth
    path("signin/", views.CustomTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    # App
    path("users/", views.UserListCreateApiView.as_view(), name="users"),
    path("students/", views.StudentListCreateApiView.as_view(), name="students"),
    path("students/<str:username>/",
         views.StudentRetrieveUpdateDestroyApiView.as_view(), name="student_details"),
    path("teachers/", views.TeacherListCreateApiView.as_view(), name="teachers"),
    path("teachers/<str:username>/",
         views.TeacherRetrieveUpdateDestroyApiView.as_view(), name="teacher_details"),

    # App 2
    path("terms/", views.TermListCreateApiView.as_view(), name="terms"),
    path("sessions/", views.SessionListCreateApiView.as_view(), name="sessions"),
    path("subjects/", views.SubjectListCreateApiView.as_view(), name="subjects"),
    path("class/", views.ClassListCreateApiView.as_view(), name="classes"),
    path("events/", views.EventListCreateApiView.as_view(), name="events"),
    path("notifications/", views.NotificationListCreateApiView.as_view(),
         name="notifications"),
    path("school_photos/", views.SchoolPhotosListCreateApiView.as_view(),
         name="school_photos"),
    path("items/", views.ItemsListCreateApiView.as_view(), name="items"),
    path("items/<str:pk>/",
         views.ItemsRetrieveUpdateDestroyApiView.as_view(), name="item_details"),
    path("scheme/", views.SchemeListCreateApiView.as_view(), name="scheme"),
    path("result/", views.ResultListCreateApiView.as_view(), name="result"),
    path("subject_result/",
         views.SubjectResultListCreateApiView.as_view(), name="subject_result"),

    path("send-email/", views.SendEmailApiView.as_view(), name="send-email"),
    path('list-emails/<str:email_type>/',
         views.ListEmailAddressesAPIView.as_view(), name='list-emails'),
]
