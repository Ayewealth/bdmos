from .models import Payment
from .models import Email
from rest_framework import serializers
from django.utils.dateformat import DateFormat
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # type: ignore
from django.core.exceptions import ObjectDoesNotExist

from .models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        data['role'] = user.role
        data['user_id'] = user.id
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Customize token payload here
        profile_id = None
        try:
            profile = StudentProfile.objects.get(user=user)
            profile_id = profile.id
        except ObjectDoesNotExist:
            pass

        # Add profile_id to the token payload
        token['profile_id'] = profile_id

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'username',
            'password',
            'role',
            'date_joined'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()
    cart = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = [
            'id',
            'user',
            'user_details',
            'results',
            'cart',
            'transactions'
        ]

    def get_user_details(self, obj):
        user_details = User.objects.filter(id=obj.user.id)
        return UserSerializer(user_details, many=True, context=self.context).data

    def get_results(self, obj):
        results = Result.objects.filter(student=obj.user)
        return ResultSerializer(results, many=True, context=self.context).data

    def get_cart(self, obj):
        cart = Cart.objects.filter(user=obj.user)
        return CartSerializer(cart, many=True, context=self.context).data

    def get_transactions(self, obj):
        transactions = Payment.objects.filter(user=obj.user)
        return PaymentSerializer(transactions, many=True, context=self.context).data


class StudentSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'username',
            'password',
            'date_of_birth',
            'sex',
            'father_name',
            'mother_name',
            'gurdian_name',
            'parents_phone_number',
            'parents_email',
            'state_of_origin',
            'religion',
            'disability',
            'student_class',
            'city_or_town',
            'previous_school',
            'disability_note',
            'passport',
            'date_joined'
        ]
        extra_kwargs = {
            'username': {'read_only': True},
            'password': {'read_only': True},
        }

    def get_date_joined(self, obj):
        return DateFormat(obj.date_joined).format('F j, Y')


class TeacherSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = [
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'username',
            'temporary_residence',
            'permanent_residence',
            'state_of_origin',
            'city_or_town',
            'sex',
            'phone_number',
            'teacher_email',
            'date_of_birth',
            'religion',
            'disability',
            'maritial_status',
            'years_of_experience',
            'computer_skills',
            'disability_note',
            'passport',
            'cv',
            'flsc',
            'waec_neco_nabteb_gce',
            'secondary_school_transcript',
            'university_polytech_institution_cer',
            'university_polytech_institution_cer_trans',
            'other_certificate',
            'teacher_speech',
            'date_joined'
        ]
        extra_kwargs = {
            'username': {'read_only': True},
        }

    def get_date_joined(self, obj):
        return DateFormat(obj.date_joined).format('F j, Y')


class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = [
            'id',
            'name',
            'phone_number',
            'email',
            'image',
            'address',
            'children_name'
        ]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'id',
            'name',
            'description'
        ]


class ClassSerializer(serializers.ModelSerializer):
    all_subjects = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = [
            'id',
            'name',
            'subjects',
            'all_subjects'
        ]

    def get_all_subjects(self, obj):
        subjects = obj.subjects.all()
        serializer = SubjectSerializer(
            instance=subjects, many=True)
        return serializer.data


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = [
            'id',
            'title',
            'price',
            'image'
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'image',
            'date',
            'description'
        ]


class SchoolPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolPhotos
        fields = [
            'id',
            'image',
            'date',
            'discription'
        ]


class NotificationTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'first_name',
            'middle_name',
            'last_name'
        ]


class NotificationSerializer(serializers.ModelSerializer):
    teachers_name = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'teacher_name',
            'teachers_name',
            'date',
            'message'
        ]

    def get_teachers_name(self, obj):
        teacher = obj.teacher_name
        serializer = NotificationTeacherSerializer(
            instance=teacher, many=False)
        return serializer.data


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = [
            'id',
            'name'
        ]


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = [
            'id',
            'name',
            'term'
        ]


class SchemeSerializer(serializers.ModelSerializer):
    term_name = serializers.SerializerMethodField()
    session_name = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()

    class Meta:
        model = Scheme
        fields = [
            'id',
            'student_class',
            'class_name',
            'term',
            'term_name',
            'session',
            'session_name',
            'date',
            'subject',
            'subject_name',
            'scheme'
        ]

    def get_subject_name(self, obj):
        subject = obj.subject
        serializer = SubjectSerializer(
            instance=subject, many=False)
        return serializer.data

    def get_class_name(self, obj):
        student_class = obj.student_class
        serializer = ClassSerializer(
            instance=student_class, many=False)
        return serializer.data

    def get_session_name(self, obj):
        session = obj.session
        serializer = SessionSerializer(
            instance=session, many=False)
        return serializer.data

    def get_term_name(self, obj):
        term = obj.term
        serializer = TermSerializer(
            instance=term, many=False)
        return serializer.data

    def validate(self, data):
        student_class = data.get('student_class')
        term = data.get('term')
        session = data.get('session')
        date = data.get('date')

        # If instance is present, exclude it from the validation query
        if Scheme.objects.filter(
            student_class=student_class,
            term=term,
            session=session,
            date=date
        ).exists():
            raise serializers.ValidationError(
                "A scheme for this class, term, session and date already exists.")

        return data


class SubjectResultSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()

    class Meta:
        model = SubjectResult
        fields = [
            'id',
            'result',
            'subject',
            'subject_name',
            'total_ca',
            'exam',
            'total',
            'grade',
            'position',
        ]

    def get_subject_name(self, obj):
        subject = obj.subject
        serializer = SubjectSerializer(
            instance=subject, many=False)
        return serializer.data


class ResultSerializer(serializers.ModelSerializer):
    subject_results = SubjectResultSerializer(many=True, required=False)
    student_name = serializers.SerializerMethodField()
    term_name = serializers.SerializerMethodField()
    session_name = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = [
            'id',
            'student',
            'student_name',
            'student_class',
            'class_name',
            'term',
            'term_name',
            'session',
            'session_name',
            'sex',
            'total_marks_obtain',
            'student_average',
            'class_average',
            'students',
            'position',
            'decision',
            'agility',
            'caring',
            'communication',
            'loving',
            'puntuality',
            'seriousness',
            'socialization',
            'attentiveness',
            'handling_of_tools',
            'honesty',
            'leadership',
            'music',
            'neatness',
            'perserverance',
            'politeness',
            'tools',
            'teacher_comment',
            'principal_comment',
            'next_term_begins',
            'next_term_school_fees',
            'subject_results',
        ]

    def get_class_name(self, obj):
        student_class = obj.student_class
        serializer = ClassSerializer(
            instance=student_class, many=False)
        return serializer.data

    def get_session_name(self, obj):
        session = obj.session
        serializer = SessionSerializer(
            instance=session, many=False)
        return serializer.data

    def get_term_name(self, obj):
        term = obj.term
        serializer = TermSerializer(
            instance=term, many=False)
        return serializer.data

    def get_student_name(self, obj):
        student = obj.student
        serializer = UserSerializer(
            instance=student, many=False)
        return serializer.data

    def get_subject_results(self, obj):
        subject_results = SubjectResult.objects.filter(result=obj)
        serializer = SubjectResultSerializer(
            instance=subject_results, many=True)
        return serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['subject_results'] = self.get_subject_results(instance)
        return representation

    def create(self, validated_data):
        subject_results_data = validated_data.pop('subject_results', [])
        result = Result.objects.create(**validated_data)
        for subject_result_data in subject_results_data:
            subject_result_data['result_id'] = result.id
            SubjectResult.objects.create(**subject_result_data)
        return result

    def validate(self, data):
        student = data.get('student')
        student_class = data.get('student_class')
        term = data.get('term')
        session = data.get('session')

        # If instance is present, exclude it from the validation query
        if self.instance:
            if Result.objects.filter(
                student=student,
                student_class=student_class,
                term=term,
                session=session
            ).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    "A result for this student, class, term, and session already exists.")
        else:
            if Result.objects.filter(
                student=student,
                student_class=student_class,
                term=term,
                session=session
            ).exists():
                raise serializers.ValidationError(
                    "A result for this student, class, term, and session already exists.")

        return data

    def update(self, instance, validated_data):
        subject_results_data = validated_data.pop('subject_results', [])

        # Update the Result instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handling SubjectResult updates
        existing_subject_results = {
            sr.id: sr for sr in instance.subjectresult_set.all()}

        for subject_result_data in subject_results_data:
            subject_result_id = subject_result_data.get('id')
            if subject_result_id and subject_result_id in existing_subject_results:
                subject_result = existing_subject_results.pop(
                    subject_result_id)
                for attr, value in subject_result_data.items():
                    setattr(subject_result, attr, value)
                subject_result.save()
            else:
                subject_result_data['result'] = instance
                SubjectResult.objects.create(**subject_result_data)

        # Delete SubjectResults that are no longer present
        for subject_result in existing_subject_results.values():
            subject_result.delete()

        return instance


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['id', 'to', 'subject', 'body', 'date']


class CartItemSerializer(serializers.ModelSerializer):
    item_data = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'item_data', 'quantity']

    def get_item_data(self, obj):
        item = obj.item
        serializer = ItemsSerializer(
            instance=item, many=False)
        return serializer.data


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(item.get_total_price() for item in obj.items.all())


class ScratchCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScratchCard
        fields = ['id', 'pin', 'usage_limit', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    session_name = serializers.SerializerMethodField()
    term_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ['id', 'user', 'fee_type', 'amount', 'status',
                  'transaction_id', 'link', 'session', 'session_name', 'term', 'term_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'status',
                            'transaction_id', 'link', 'created_at', 'updated_at']

    def get_session_name(self, obj):
        session = obj.session
        serializer = SessionSerializer(
            instance=session, many=False)
        return serializer.data

    def get_term_name(self, obj):
        term = obj.term
        serializer = TermSerializer(
            instance=term, many=False)
        return serializer.data


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bills
        fields = [
            "id",
            "name"
        ]


class StudentPasswordSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = StudentPassword
        fields = [
            "id",
            "student",
            "student_name",
            "raw_password"
        ]

    def get_student_name(self, obj):
        student = obj.student
        serializer = UserSerializer(
            instance=student, many=False)
        return serializer.data


class TeacherApplicationSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    middle_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    last_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    username = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    temporary_residence = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    permanent_residence = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    state_of_origin = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    city_or_town = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    sex = serializers.CharField(
        max_length=10, required=False, allow_blank=True)
    phone_number = serializers.CharField(
        max_length=20, required=False, allow_blank=True)
    teacher_email = serializers.EmailField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    religion = serializers.CharField(
        max_length=50, required=False, allow_blank=True)
    disability = serializers.CharField(
        max_length=10, required=False, allow_blank=True)
    maritial_status = serializers.CharField(
        max_length=20, required=False, allow_blank=True)
    years_of_experience = serializers.IntegerField(
        required=False, allow_null=True,)
    computer_skills = serializers.CharField(
        max_length=10, required=False, allow_blank=True)
    disability_note = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    passport = serializers.FileField(required=False)
    cv = serializers.FileField(required=False)
    flsc = serializers.FileField(required=False)
    waec_neco_nabteb_gce = serializers.FileField(
        required=False)
    secondary_school_transcript = serializers.FileField(
        required=False)
    university_polytech_institution_cer = serializers.FileField(
        required=False)
    university_polytech_institution_cer_trans = serializers.FileField(
        required=False)
    other_certificate = serializers.FileField(required=False)
    teacher_speech = serializers.CharField(required=False)


class StudentApplicationSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    middle_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    last_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    username = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    father_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    mother_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    gurdian_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    parents_phone_number = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    parents_email = serializers.EmailField(
        max_length=255, required=False, allow_blank=True)
    state_of_origin = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    religion = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    disability = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    disability_note = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    city_or_town = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    previous_school = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    student_class = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    passport = serializers.FileField(required=False)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
