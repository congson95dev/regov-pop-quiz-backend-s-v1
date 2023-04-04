from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from quiz.models import Course, CourseEnroll
from quiz.serializers import CourseSerializer, CourseEnrollCreateSerializer, CourseEnrollUpdateSerializer


class CourseViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    GenericViewSet):
    def get_queryset(self):
        queryset = Course.objects.prefetch_related("course_enroll").all()
        return queryset
    serializer_class = CourseSerializer


class CourseEnrollViewSet(mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          GenericViewSet):
    queryset = CourseEnroll.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CourseEnrollUpdateSerializer
        return CourseEnrollCreateSerializer

    def get_serializer_context(self):
        return {'course_id': self.kwargs['course_pk']}
