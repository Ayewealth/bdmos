from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Group as AuthGroup, Permission as AuthPermission
from django.utils import timezone
import random
import uuid

# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name


class Class(models.Model):
    CLASS_CHOICES = [
        ('Learning Development Class', 'Learning Development Class'),
        ('Nursery 1', 'Nursery 1'),
        ('Nursery 2', 'Nursery 2'),
        ('Nursery 3', 'Nursery 3'),
        ('Primary 1', 'Primary 1'),
        ('Primary 2', 'Primary 2'),
        ('Primary 3', 'Primary 3'),
        ('Primary 4', 'Primary 4'),
        ('Primary 5', 'Primary 5'),
        ('Primary 6', 'Primary 6'),
        ('Primary 7', 'Primary 7'),
        ('Primary 8', 'Primary 8'),
        ('Primary 9', 'Primary 9'),
    ]

    name = models.CharField(max_length=50, choices=CLASS_CHOICES)
    subjects = models.ManyToManyField(
        Subject, blank=True, related_name='classes')

    class Meta:
        verbose_name_plural = "Class"

    def __str__(self):
        return self.name


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    date_joined = models.DateTimeField(default=timezone.now)

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"

    role = models.CharField(
        max_length=50, choices=Role.choices, default=Role.ADMIN)

    class Meta:
        verbose_name_plural = "Users"


class Student(User):
    DISABILITY = [
        ('yes', 'YES'),
        ('no', 'NO'),
    ]

    RELIGIONS = [
        ("christian", "CHRISTIAN"),
        ("muslim", "MUSLIM"),
        ("others", "OTHERS")
    ]

    SEX = [
        ("male", "MALE"),
        ("female", "FEMALE")
    ]

    sex = models.CharField(max_length=50, blank=True, null=True, choices=SEX)

    father_name = models.CharField(max_length=255, blank=True, null=True)
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    gurdian_name = models.CharField(max_length=255, blank=True, null=True)
    parents_phone_number = models.CharField(
        max_length=11, blank=True, null=True)
    parents_email = models.EmailField(blank=True, null=True)

    state_of_origin = models.CharField(max_length=100, blank=True, null=True)
    religion = models.CharField(max_length=30, choices=RELIGIONS)
    disability = models.CharField(max_length=20, choices=DISABILITY)
    disability_note = models.TextField(null=True, blank=True)
    city_or_town = models.CharField(max_length=255, blank=True, null=True)
    previous_school = models.CharField(max_length=255, blank=True, null=True)
    student_class = models.ForeignKey(
        Class, null=True, blank=True, on_delete=models.CASCADE)
    passport = models.ImageField(upload_to="student_passport", null=True)

    date_of_birth = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Students"

    def save(self, *args, **kwargs):
        if not self.pk:
            generated_username = self.first_name.lower() + str(random.randint(1000, 9999))
            last_name_initial = self.last_name.lower()[
                0] if self.last_name else ""
            generated_password = self.first_name.lower() + last_name_initial + \
                str(random.randint(1000, 9999))
            self._generated_username = generated_username
            self._generated_password = generated_password

            self.role = User.Role.STUDENT
            self.username = generated_username
            self.set_password(generated_password)

        super().save(*args, **kwargs)


class Teacher(User):
    DISABILITY = [
        ('yes', 'YES'),
        ('no', 'NO'),
    ]
    RELIGIONS = [
        ("christian", "CHRISTIAN"),
        ("muslim", "MUSLIM"),
        ("others", "OTHERS")
    ]
    SEX = [
        ("male", "MALE"),
        ("female", "FEMALE")
    ]
    MARITIAL_STATUS = [
        ("married", "MARRIED"),
        ("single", "SINGLE")
    ]
    COMPUTER_SKILLS = [
        ("yes", "YES"),
        ("no", "NO")
    ]

    temporary_residence = models.CharField(
        max_length=255, null=True, blank=True)
    permanent_residence = models.CharField(
        max_length=255, null=True, blank=True)
    state_of_origin = models.CharField(max_length=100, blank=True, null=True)
    city_or_town = models.TextField(max_length=255, blank=True, null=True)
    sex = models.CharField(max_length=50, blank=True, null=True, choices=SEX)
    phone_number = models.IntegerField(blank=True, null=True)
    teacher_email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    religion = models.CharField(
        max_length=30,  blank=True, null=True, choices=RELIGIONS)
    disability = models.CharField(
        max_length=20, blank=True, null=True, choices=DISABILITY)
    maritial_status = models.CharField(
        max_length=20,  blank=True, null=True, choices=MARITIAL_STATUS)
    years_of_experience = models.CharField(
        max_length=50, null=True, blank=True)
    computer_skills = models.CharField(
        max_length=20,  blank=True, null=True, choices=COMPUTER_SKILLS)
    disability_note = models.TextField(null=True, blank=True)
    passport = models.ImageField(upload_to="teachers_passport", null=True)
    cv = models.FileField(upload_to="cv's", null=True)
    flsc = models.FileField(
        upload_to="teacher_documents", null=True)
    waec_neco_nabteb_gce = models.FileField(
        upload_to="teacher_documents", null=True)
    secondary_school_transcript = models.FileField(
        upload_to="teacher_documents", null=True)
    university_polytech_institution_cer = models.FileField(
        upload_to="teacher_documents", null=True)
    university_polytech_institution_cer_trans = models.FileField(
        upload_to="teacher_documents", null=True)
    other_certificate = models.FileField(
        upload_to="other_certificate", null=True)

    teacher_speech = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Teachers"

    def save(self, *args, **kwargs):
        if not self.pk:
            generated_username = self.first_name.lower() + str(random.randint(1000, 9999))

            self.role = User.Role.TEACHER
            self._generated_username = generated_username
            self.username = generated_username

        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return False

    def has_module_perms(self, app_label):
        return False


class Items(models.Model):
    image = models.ImageField(upload_to="images", null=True)
    title = models.CharField(max_length=30, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Items"

    def __str__(self):
        return self.title


class Event(models.Model):
    image = models.ImageField(upload_to="event", null=True)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Event {self._id}"


class Notification(models.Model):
    teacher_name = models.ForeignKey(
        Teacher, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Notification By {self.teacher_name}"


class SchoolPhotos(models.Model):
    image = models.ImageField(upload_to="school_gallery", null=True)
    date = models.DateField(null=True, blank=True)
    discription = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "School Photos"

    def __str__(self):
        return f"Photo {self._id}"


class Term(models.Model):
    TERMS = [
        ("first term", "FIRST TERM"),
        ("second term", "SECOND TERM"),
        ("third term", "THIRD TERM")
    ]
    name = models.CharField(max_length=50, blank=True,
                            null=True, choices=TERMS)

    def __str__(self):
        return self.name


class Session(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    term = models.ManyToManyField(Term,  related_name="terms")

    def __str__(self):
        return self.name


class Scheme(models.Model):
    student_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, null=True, blank=True)
    term = models.ForeignKey(
        Term, on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, null=True, blank=True)
    scheme = models.FileField()

    def __str__(self):
        return f"{self.subject} scheme"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, through='SubjectResult')

    class Meta:
        verbose_name_plural = "Results"

    def __str__(self):
        return f"{self.student} - {self.term} - {self.session} Result"


class SubjectResult(models.Model):
    result = models.ForeignKey(Result, null=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_ca = models.FloatField(
        null=True, blank=True, verbose_name='Total C.A. Score (40%)')
    exam = models.FloatField(
        null=True, blank=True, verbose_name='EXAM (60%)')
    total = models.FloatField(
        null=True, blank=True, verbose_name='TOTAL (100%)')
    grade = models.CharField(max_length=10, null=True, blank=True)
    position = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Subject Results"

    def __str__(self):
        return f"{self.result.student} - {self.subject} - Result"
