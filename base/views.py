from .serializers import *
from .models import *
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
from django.utils.crypto import get_random_string
from .flutterwave import initialize_payment, verify_payment
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
import logging
import json

logger = logging.getLogger(__name__)

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
        "check_scheme/",
        "result/",
        "check_result/",
        "subject_result/",
        "send-email/",
        "list-emails/<str:email_type>/",
        "cart/",
        "cart/add/",
        "scratch_cards/",
        "bills/",
        "bills/id/",
        "payments/",
        "payments-callback/",
        "all_payments/",
        "transactions/status_type/",
        "student_passwords/",
        "send-teacher-application-email/"
    ]
    return Response(data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserListCreateApiView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileListApiView(generics.ListAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileRetriveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'


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

        StudentPassword.objects.create(
            student=instance, raw_password=generated_password)

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
    permission_classes = [IsAuthenticated]
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['subject__name']

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


class CheckScheme(generics.ListCreateAPIView):
    serializer_class = SchemeSerializer

    def get_queryset(self):
        student_class = self.request.query_params.get('student_class')
        session = self.request.query_params.get('session')
        term = self.request.query_params.get('term')

        queryset = Scheme.objects.all()

        if student_class:
            queryset = queryset.filter(student_class=student_class)
        if session:
            queryset = queryset.filter(session=session)
        if term:
            queryset = queryset.filter(term=term)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'error': 'No Scheme found for the specified session and term'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SchemeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    permission_classes = [IsAuthenticated]


class CartRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

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


class GenerateScratchCardView(generics.ListCreateAPIView):
    queryset = ScratchCard.objects.all()
    serializer_class = ScratchCardSerializer

    def create(self, request, *args, **kwargs):
        amount = int(request.data.get('amount', 1))
        cards = []
        for _ in range(amount):
            pin = get_random_string(12, '0123456789')
            card = ScratchCard.objects.create(pin=pin)
            cards.append(card)
        serializer = ScratchCardSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckResultView(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        pin = request.data.get('pin')
        session = request.data.get('session')
        term = request.data.get('term')
        student_class = request.data.get('class')

        try:
            card = ScratchCard.objects.get(pin=pin)
        except ScratchCard.DoesNotExist:
            return Response({'error': 'Invalid scratch card pin'}, status=status.HTTP_400_BAD_REQUEST)

        if card.usage_limit <= 0:
            return Response({'error': 'Scratch card usage limit exceeded'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = User.objects.get(
                username=username, role=User.Role.STUDENT)
        except User.DoesNotExist:
            return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)

        results = Result.objects.filter(
            student=student, student_class=student_class, session=session, term=term)
        if not results:
            return Response({'error': 'No results found for the specified session and term'}, status=status.HTTP_404_NOT_FOUND)

        card.usage_limit -= 1
        card.save()

        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BillListCreateView(generics.ListCreateAPIView):
    queryset = Bills.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]


class BillRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bills.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentSerializer
        return PaymentSerializer

    def perform_create(self, serializer):
        user = self.request.user
        fee_type_id = self.request.data.get("fee_type")
        amount = self.request.data.get("amount")
        tx_ref = str(random.randint(1000, 9999))

        if not hasattr(user, 'student'):
            return Response({"detail": "User is not a student"}, status=status.HTTP_400_BAD_REQUEST)

        student = get_object_or_404(Student, id=user.id)
        fee_type = get_object_or_404(Bills, id=fee_type_id)

        response, data = initialize_payment(amount, student, fee_type, tx_ref)
        print(data)
        if response.status_code == 200 and data:
            # Save payment instance with data from Flutterwave
            payment = serializer.save(
                user=student,
                fee_type=fee_type,
                amount=amount,
                transaction_id=f"{student.username}-{tx_ref}",
                link=data['data']['link'],
                status='Pending'
            )
            payment.save()
        else:
            error_message = data.get(
                'message', 'Failed to initialize payment') if data else 'Failed to initialize payment: No response data'
            logger.error(f"Payment initialization error: {error_message}")
            raise ValidationError(error_message)


@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failed', 'message': 'Invalid JSON data'}, status=400)

        transaction_id = data['data']['transaction_id']
        tx_ref = data['data']['tx_ref']
        response, payment_data = verify_payment(transaction_id)
        if response.status_code == 200:
            payment = Payment.objects.get(transaction_id=tx_ref)
            if payment_data['status'] == 'success':
                payment.status = 'Approved'
            else:
                payment.status = 'Declined'
            payment.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Verification failed'}, status=400)

    elif request.method == 'GET':
        transaction_id = request.GET.get('transaction_id')
        tx_ref = request.GET.get('tx_ref')
        if not transaction_id:
            return JsonResponse({'status': 'failed', 'message': 'No transaction ID provided'}, status=400)

        response, payment_data = verify_payment(transaction_id)
        if response.status_code == 200:
            payment = Payment.objects.get(transaction_id=tx_ref)
            if payment_data['status'] == 'success':
                payment.status = 'Approved'
            else:
                payment.status = 'Declined'
            payment.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Verification failed'}, status=400)

    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)


class AllPaymentsListApiView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ListTransactionsPaymentView(APIView):
    def get(self, request, *args, **kwargs):
        status_type = self.kwargs.get('status_type')

        if status_type == 'approved':
            transactions = Payment.objects.filter(status="Approved")
        elif status_type == 'declined':
            transactions = Payment.objects.filter(status="Declined")
        elif status_type == 'pending':
            transactions = Payment.objects.filter(status="Pending")
        else:
            return Response({"error": "Invalid status type."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PaymentSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentPasswordListCreateApiView(generics.ListCreateAPIView):
    queryset = StudentPassword.objects.all()
    serializer_class = StudentPasswordSerializer


class SendTeacherApplicationEmailView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.GET.get("teacher_email")
        serializer = TeacherApplicationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            admin_email = settings.DEFAULT_FROM_EMAIL

            subject = "New Teacher Application Submission"
            from_email = email
            to_email = admin_email

            # Create email content
            text_content = f"""
                New teacher application received:
                First Name: {data.get('first_name', 'N/A')}
                Middle Name: {data.get('middle_name', 'N/A')}
                Last Name: {data.get('last_name', 'N/A')}
                Username: {data.get('username', 'N/A')}
                Temporary Residence: {data.get('temporary_residence', 'N/A')}
                Permanent Residence: {data.get('permanent_residence', 'N/A')}
                State of Origin: {data.get('state_of_origin', 'N/A')}
                City or Town: {data.get('city_or_town', 'N/A')}
                Sex: {data.get('sex', 'N/A')}
                Phone Number: {data.get('phone_number', 'N/A')}
                Teacher Email: {data.get('teacher_email', 'N/A')}
                Date of Birth: {data.get('date_of_birth', 'N/A')}
                Religion: {data.get('religion', 'N/A')}
                Disability: {data.get('disability', 'N/A')}
                Marital Status: {data.get('maritial_status', 'N/A')}
                Years of Experience: {data.get('years_of_experience', 'N/A')}
                Computer Skills: {data.get('computer_skills', 'N/A')}
                Disability Note: {data.get('disability_note', 'N/A')}
                Passport: {data.get('passport', 'N/A')}
                CV: {data.get('cv', 'N/A')}
                FSLC: {data.get('flsc', 'N/A')}
                WAEC/NECO/NABTEB/GCE: {data.get('waec_neco_nabteb_gce', 'N/A')}
                Secondary School Transcript: {data.get('secondary_school_transcript', 'N/A')}
                University/Polytechnic Institution Certificate: {data.get('university_polytech_institution_cer', 'N/A')}
                University/Polytechnic Institution Certificate Transcript: {data.get('university_polytech_institution_cer_trans', 'N/A')}
                Other Certificate: {data.get('other_certificate', 'N/A')}
                Teacher Speech: {data.get('teacher_speech', 'N/A')}
            """

            html_content = f"""
                <html>
                    <body>
                        <p>New teacher application received:</p>
                        <ul>
                            <li><strong>First Name:</strong> {data.get('first_name', 'N/A')}</li>
                            <li><strong>Middle Name:</strong> {data.get('middle_name', 'N/A')}</li>
                            <li><strong>Last Name:</strong> {data.get('last_name', 'N/A')}</li>
                            <li><strong>Username:</strong> {data.get('username', 'N/A')}</li>
                            <li><strong>Temporary Residence:</strong> {data.get('temporary_residence', 'N/A')}</li>
                            <li><strong>Permanent Residence:</strong> {data.get('permanent_residence', 'N/A')}</li>
                            <li><strong>State of Origin:</strong> {data.get('state_of_origin', 'N/A')}</li>
                            <li><strong>City or Town:</strong> {data.get('city_or_town', 'N/A')}</li>
                            <li><strong>Sex:</strong> {data.get('sex', 'N/A')}</li>
                            <li><strong>Phone Number:</strong> {data.get('phone_number', 'N/A')}</li>
                            <li><strong>Teacher Email:</strong> {data.get('teacher_email', 'N/A')}</li>
                            <li><strong>Date of Birth:</strong> {data.get('date_of_birth', 'N/A')}</li>
                            <li><strong>Religion:</strong> {data.get('religion', 'N/A')}</li>
                            <li><strong>Disability:</strong> {data.get('disability', 'N/A')}</li>
                            <li><strong>Marital Status:</strong> {data.get('maritial_status', 'N/A')}</li>
                            <li><strong>Years of Experience:</strong> {data.get('years_of_experience', 'N/A')}</li>
                            <li><strong>Computer Skills:</strong> {data.get('computer_skills', 'N/A')}</li>
                            <li><strong>Disability Note:</strong> {data.get('disability_note', 'N/A')}</li>
                            <li><strong>Passport:</strong> <a href="{data.get('passport', 'N/A')}">View Passport</a></li>
                            <li><strong>CV:</strong> <a href="{data.get('cv', 'N/A')}">View CV</a></li>
                            <li><strong>FSLC:</strong> <a href="{data.get('flsc', 'N/A')}">View FSLC</a></li>
                            <li><strong>WAEC/NECO/NABTEB/GCE:</strong> <a href="{data.get('waec_neco_nabteb_gce', 'N/A')}">View Document</a></li>
                            <li><strong>Secondary School Transcript:</strong> <a href="{data.get('secondary_school_transcript', 'N/A')}">View Transcript</a></li>
                            <li><strong>University/Polytechnic Institution Certificate:</strong> <a href="{data.get('university_polytech_institution_cer', 'N/A')}">View Certificate</a></li>
                            <li><strong>University/Polytechnic Institution Certificate Transcript:</strong> <a href="{data.get('university_polytech_institution_cer_trans', 'N/A')}">View Transcript</a></li>
                            <li><strong>Other Certificate:</strong> <a href="{data.get('other_certificate', 'N/A')}">View Certificate</a></li>
                            <li><strong>Teacher Speech:</strong> {data.get('teacher_speech', 'N/A')}</li>
                        </ul>
                    </body>
                </html>
            """

            # Create the email
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")

            # Send the email
            msg.send()

            return Response({"message": "Application submitted successfully and email sent to admin."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
