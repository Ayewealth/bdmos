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

    path("parents/", views.ParentsListCreateApiView.as_view(), name="parents"),
    path("parents/<str:pk>/",
         views.ParentsRetrieveUpdateDestroyApiView.as_view(), name="parents-details"),

    # App 2
    path("terms/", views.TermListCreateApiView.as_view(), name="terms"),
    path("terms/<str:pk>/",
         views.TermRetrieveUpdateDestroyApiView.as_view(), name="terms-details"),

    path("sessions/", views.SessionListCreateApiView.as_view(), name="sessions"),
    path("sessions/<str:pk>/",
         views.SessionRetrieveUpdateDestroyApiView.as_view(), name="sessions-details"),

    path("subjects/", views.SubjectListCreateApiView.as_view(), name="subjects"),
    path("subjects/<str:pk>/",
         views.SubjectRetrieveUpdateDestroyApiView.as_view(), name="subjects-details"),

    path("class/", views.ClassListCreateApiView.as_view(), name="classes"),
    path("class/<str:name>/",
         views.ClassRetrieveUpdateDestroyApiView.as_view(), name="classes-details"),

    path("events/", views.EventListCreateApiView.as_view(), name="events"),
    path("events/<str:pk>/",
         views.EventRetrieveUpdateDestroyApiView.as_view(), name="events-details"),

    path("notifications/", views.NotificationListCreateApiView.as_view(),
         name="notifications"),
    path("notifications/<str:pk>/", views.NotificationRetrieveUpdateDestroyApiView.as_view(),
         name="notifications-details"),

    path("school_photos/", views.SchoolPhotosListCreateApiView.as_view(),
         name="school_photos"),
    path("school_photos/<str:pk>/", views.SchoolPhotosRetrieveUpdateDestroyApiView.as_view(),
         name="school_photos-details"),

    path("items/", views.ItemsListCreateApiView.as_view(), name="items"),
    path("items/<str:pk>/",
         views.ItemsRetrieveUpdateDestroyApiView.as_view(), name="item_details"),

    path("scheme/", views.SchemeListCreateApiView.as_view(), name="scheme"),
    path("scheme/<str:pk>/",
         views.SchemeRetrieveUpdateDestroyApiView.as_view(), name="scheme-details"),

    path("result/", views.ResultListCreateApiView.as_view(), name="result"),
    path("result/<str:pk>/",
         views.ResultRetrieveUpdateDestroyApiView.as_view(), name="result-details"),

    path("subject_result/",
         views.SubjectResultListCreateApiView.as_view(), name="subject_result"),
    path("subject_result/<str:pk>/",
         views.SubjectResultRetrieveUpdateDestroyApiView.as_view(), name="subject_result-details"),

    path("send-email/", views.SendEmailApiView.as_view(), name="send-email"),
    path('list-emails/<str:email_type>/',
         views.ListEmailAddressesAPIView.as_view(), name='list-emails'),
]
