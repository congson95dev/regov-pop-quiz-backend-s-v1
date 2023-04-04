import datetime

from django.db import transaction
from rest_framework import serializers

from quiz.models import Course, Student, CourseEnroll


class CourseStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'firstname', 'lastname', 'email', 'phone', 'birth_date']


class CourseEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnroll
        fields = ['id']

    # student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())


class CourseSerializer(serializers.ModelSerializer):
    student_enrolled = CourseEnrollSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'capacity', 'number_student_enrolled', 'student_enrolled']

    number_student_enrolled = serializers.SerializerMethodField(method_name='calculate_number_student_enrolled')

    # if "student_enrolled" >= "capacity", FE will disable the enroll button
    # we will comeback and resolve the duplicate query later
    def calculate_number_student_enrolled(self, course: Course):
        return course.course_enroll.filter(deleted_date__isnull=True).count()


class CourseEnrollCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnroll
        fields = ['id', 'student']

    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    def create(self, validated_data):
        with transaction.atomic():
            course_id = self.context['course_id']
            return CourseEnroll.objects.create(course_id=course_id, **validated_data)


class CourseEnrollUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnroll
        fields = ['id']

    def update(self, instance, validated_data):
        if instance.deleted_date:
            raise serializers.ValidationError('You have already drop this course')
        with transaction.atomic():
            # soft delete
            instance.deleted_date = datetime.datetime.now()
            instance.save()
            return instance
