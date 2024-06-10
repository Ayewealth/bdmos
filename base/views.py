from rest_framework.views import APIView
from .models import Student, Teacher
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView  # type: ignore
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .utils import send_single_email, send_bulk_email
from rest_framework import status

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
        "scheme/",
        "result/",
        "subject_result/",
        "send-email/",
        "list-emails/<str:email_type>/",
        "cart/",
        "cart/add/"
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
    # permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name',
                     'last_name', "student_class__name"]

    def perform_create(self, serializer):
        instance = serializer.save()

        generated_username = serializer.data.get('username')
        generated_password = instance._generated_password
        parents_email = instance.parents_email
        gurdian_name = instance.gurdian_name

        print("Generated Username:", generated_username)
        print("Generated Password:", generated_password)

        if parents_email:
            subject = 'Welcome to BDMOS! Access Your Child\'s Portal with These Credentials.'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = parents_email

            # Plain text content
            text_content = f"""
                                Dear {gurdian_name},

                                We are delighted to welcome you and your child to BDMOS. Our heartfelt gratitude goes out to you for entrusting us with your child's education and well-being.

                                To help you stay informed about your child's academic progress and school activities, we have created a dedicated portal for parents. Below are the login credentials you will need to access your child's portal:

                                Username: {generated_username}
                                Password: {generated_password}

                                Please use these credentials to log in at https://bdmos-frontend.vercel.app/. Should you have any questions or require assistance, do not hesitate to reach out to us.

                                Thank you once again for being a valued part of our school community. We look forward to a successful and enriching school year ahead.

                                Warm regards,
                            """

            # HTML content
            html_content = f"""
                                <html>
                                    <body>
                                        <p>Dear {gurdian_name},</p>

                                        <p>We are delighted to welcome you and your child to BDMOS. Our heartfelt gratitude goes out to you for entrusting us with your child's education and well-being.</p>

                                        <p>To help you stay informed about your child's academic progress and school activities, we have created a dedicated portal for parents. Below are the login credentials you will need to access your child's portal:</p>

                                        <p><strong>Username:</strong> {generated_username}<br>
                                        <strong>Password:</strong> {generated_password}</p>

                                        <p>Please use these credentials to log in at <a href="https://bdmos-frontend.vercel.app/">this portal link</a>. Should you have any questions or require assistance, do not hesitate to reach out to us.</p>

                                        <p>Thank you once again for being a valued part of our school community. We look forward to a successful and enriching school year ahead.</p>

                                        <p>Warm regards,</p>
                                    </body>
                                </html>
                             """

            # Create the email
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")

            # Send the email
            msg.send()

        return instance


class StudentRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated]


class TeacherListCreateApiView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', "phone_number"]

    def perform_create(self, serializer):
        instance = serializer.save()

        generated_username = serializer.data.get('username')

        print("Generated Username:", generated_username)

        return instance


class TeacherRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated]


class ParentsListCreateApiView(generics.ListCreateAPIView):
    queryset = Parents.objects.all()
    serializer_class = ParentsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone_number']


class ParentsRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parents.objects.all()
    serializer_class = ParentsSerializer
    lookup_field = 'pk'


class TermListCreateApiView(generics.ListCreateAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer


class TermRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    lookup_field = "pk"


class SessionListCreateApiView(generics.ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class SessionRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    lookup_field = "pk"


class SubjectListCreateApiView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class SubjectRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    lookup_field = "pk"


class ClassListCreateApiView(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ClassRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    lookup_field = "pk"


class EventListCreateApiView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['date', 'description']


class EventRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "pk"


class NotificationListCreateApiView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['teacher_name__first_name', 'date']


class NotificationRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    lookup_field = "pk"


class SchoolPhotosListCreateApiView(generics.ListCreateAPIView):
    queryset = SchoolPhotos.objects.all()
    serializer_class = SchoolPhotosSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['date']


class SchoolPhotosRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SchoolPhotos.objects.all()
    serializer_class = SchoolPhotosSerializer
    lookup_field = "pk"


class ItemsListCreateApiView(generics.ListCreateAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'price']
    permission_classes = [IsAuthenticated]


class ItemsRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    lookup_field = 'pk'


class SchemeListCreateApiView(generics.ListCreateAPIView):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super().create(request, *args, **kwargs)


class SchemeRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer
    lookup_field = "pk"


class ResultListCreateApiView(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['term', 'session']
    search_fields = ['student__username']


class ResultRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    lookup_field = "pk"


class SubjectResultListCreateApiView(generics.ListCreateAPIView):
    queryset = SubjectResult.objects.all()
    serializer_class = SubjectResultSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(data := kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)


class SubjectResultRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubjectResult.objects.all()
    serializer_class = SubjectResultSerializer
    lookup_field = "pk"


class SendEmailApiView(generics.ListCreateAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['to']

    def post(self, request, *args, **kwargs):
        to_email = request.data.get('to')
        subject = request.data.get('subject')
        body = request.data.get('body')
        is_bulk = request.data.get('is_bulk', False)

        if is_bulk:
            if not isinstance(to_email, list):
                return Response({"error": "For bulk emails, 'to' should be a list of email addresses."}, status=status.HTTP_400_BAD_REQUEST)
            success = send_bulk_email(to_email, subject, body)
        else:
            if not isinstance(to_email, str):
                return Response({"error": "For single email, 'to' should be a single email address."}, status=status.HTTP_400_BAD_REQUEST)
            success = send_single_email(to_email, subject, body)

        if success:
            return Response({"message": "Email(s) sent successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to send email(s)."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SendEmailRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    lookup_field = "pk"


class ListEmailAddressesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        email_type = self.kwargs.get('email_type')

        if email_type == 'parents':
            email_addresses = Student.objects.exclude(parents_email__isnull=True).exclude(
                parents_email__exact='').values_list('parents_email', flat=True).distinct()
        elif email_type == 'teachers':
            email_addresses = Teacher.objects.exclude(teacher_email__isnull=True).exclude(
                teacher_email__exact='').values_list('teacher_email', flat=True).distinct()
        else:
            return Response({"error": "Invalid email type."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"email_addresses": list(email_addresses)}, status=status.HTTP_200_OK)


class CartListCreateApiView(generics.ListCreateAPIView):
    queryset = Cart
    serializer_class = CartSerializer


class CartRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart
    serializer_class = CartSerializer

    def get_object(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart


class AddToCartView(generics.GenericAPIView):
    serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        item_id = request.data.get('item')
        quantity = request.data.get('quantity', 1)

        try:
            item = Items.objects.get(id=item_id)
        except Items.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(user=user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, item=item)
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        return Response({"message": "Item added to cart."}, status=status.HTTP_200_OK)
