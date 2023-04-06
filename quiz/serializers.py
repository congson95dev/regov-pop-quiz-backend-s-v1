import datetime

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from quiz.models import Course, Student, CourseEnroll


class CourseStudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CourseStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user_id', 'user', 'phone', 'birth_date']

    user = CourseStudentUserSerializer(read_only=True)


class CourseEnrollSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnroll
        fields = ['id', 'student']

    student = CourseStudentSerializer(read_only=True)


class CourseSerializer(serializers.ModelSerializer):
    # nested serializer to show list student that enroll in particular course
    course_enroll = CourseEnrollSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'capacity', 'course_enroll']


class CoursesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'title', 'capacity', 'number_student_enrolled']

    number_student_enrolled = serializers.SerializerMethodField(method_name='calculate_number_student_enrolled')

    # if "student_enrolled" >= "capacity", FE will disable the enroll button
    def calculate_number_student_enrolled(self, course: Course):
        return course.course_enroll.filter(deleted_date__isnull=True).count()


class CourseEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnroll
        fields = ['id', 'student', 'course']

    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        with transaction.atomic():
            course_id = self.context['course_id']
            course_enrolled = CourseEnroll.objects\
                .filter(course_id=course_id, student_id=validated_data.get('student').id)\
                .exists()
            if course_enrolled:
                raise serializers.ValidationError('You have already enroll this course')
            return CourseEnroll.objects.create(course_id=course_id, **validated_data)


class CourseEnrollUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnroll
        fields = ['id']

    def update(self, instance, validated_data):
        if instance.deleted_date:
            raise serializers.ValidationError('You have already drop this course')
        if instance.course_id != self.context['course_id']:
            raise serializers.ValidationError('This course dont have this enroll id')
        with transaction.atomic():
            # soft delete
            instance.deleted_date = datetime.datetime.now()
            instance.save()
            return instance
