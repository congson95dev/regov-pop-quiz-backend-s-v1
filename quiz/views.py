from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from quiz.models import Course, CourseEnroll
from quiz.pagination import CustomPagination
from quiz.permissions import IsStudent, IsAdmin
from quiz.serializers import CourseSerializer, CourseEnrollSerializer, CourseEnrollUpdateSerializer, \
    CoursesSerializer


class CoursesViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     GenericViewSet):
    pagination_class = CustomPagination
    serializer_class = CoursesSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Course.objects.prefetch_related("course_enroll").all()
        return queryset


class CourseViewSet(mixins.RetrieveModelMixin,
                    GenericViewSet):
    serializer_class = CourseSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Course.objects.prefetch_related("course_enroll__student__user").all()
        return queryset


class CourseEnrollViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          GenericViewSet):
    queryset = CourseEnroll.objects.filter(deleted_date__isnull=True).all()
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method in ('POST', 'PUT'):
            return [IsAuthenticated(), IsStudent()]
        return [IsAuthenticated(), IsAdmin()]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CourseEnrollUpdateSerializer
        return CourseEnrollSerializer

    def get_serializer_context(self):
        if self.kwargs.get('pk') is not None:
            return {'course_id': self.kwargs['course_pk'], 'student_id': self.kwargs['pk']}
        else:
            return {'course_id': self.kwargs['course_pk']}


class CourseDropViewSet(mixins.ListModelMixin,
                        GenericViewSet):
    queryset = CourseEnroll.objects.filter(deleted_date__isnull=False).all()
    pagination_class = CustomPagination

    def get_permissions(self):
        return [IsAuthenticated(), IsAdmin()]

    def get_serializer_class(self):
        return CourseEnrollSerializer
