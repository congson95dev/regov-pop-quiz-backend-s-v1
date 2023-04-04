from django.contrib.auth import get_user_model
from django.db import models


class Student(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    birth_date = models.DateField(null=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)


class Administrator(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)


class Course(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    capacity = models.IntegerField(default=50)


class CourseEnroll(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='course_enroll')
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='student_enroll')
    deleted_date = models.DateTimeField(null=True)

