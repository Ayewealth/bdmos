from .models import Email
from rest_framework import serializers
from django.utils.dateformat import DateFormat
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # type: ignore

from .models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        data['role'] = user.role

        return data


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


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'teacher_name',
            'date',
            'message'
        ]


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
    class Meta:
        model = Scheme
        fields = [
            'id',
            'student_class',
            'term',
            'session',
            'date',
            'subject',
            'scheme'
        ]


class SubjectResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectResult
        fields = [
            'id',
            'result',
            'subject',
            'total_ca',
            'exam',
            'total',
            'grade',
            'position',
        ]


class ResultSerializer(serializers.ModelSerializer):
    subject_results = SubjectResultSerializer(many=True, required=False)

    class Meta:
        model = Result
        fields = [
            'id',
            'student',
            'student_class',
            'term',
            'session',
            'sex',
            "total_marks_obtain",
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

    def update(self, instance, validated_data):
        subject_results_data = validated_data.pop('subject_results', [])
        subject_results = instance.subject_results.all()
        subject_results = list(subject_results)
        instance.student = validated_data.get('student', instance.student)
        instance.student_class = validated_data.get(
            'student_class', instance.student_class)
        instance.term = validated_data.get('term', instance.term)
        instance.session = validated_data.get('session', instance.session)
        instance.save()

        for subject_result_data in subject_results_data:
            subject_result = subject_results.pop(0)
            subject_result.subject = subject_result_data.get(
                'subject', subject_result.subject)
            subject_result.total_ca = subject_result_data.get(
                'total_ca', subject_result.total_ca)
            subject_result.exam = subject_result_data.get(
                'exam', subject_result.exam)
            subject_result.total = subject_result_data.get(
                'total', subject_result.total)
            subject_result.grade = subject_result_data.get(
                'grade', subject_result.grade)
            subject_result.position = subject_result_data.get(
                'position', subject_result.position)
            subject_result.save()

        return instance


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['to', 'subject', 'body', 'date']
