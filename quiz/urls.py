from rest_framework_nested import routers

from quiz import views

router = routers.DefaultRouter()
router.register('courses', views.CoursesViewSet, basename='courses')
router.register('course', views.CourseViewSet, basename='course')
router.register('drops', views.CourseDropViewSet, basename='drops')


course_router = routers.NestedSimpleRouter(router, 'courses', lookup='course')
course_router.register(r'course_enroll', views.CourseEnrollViewSet, basename='course_enroll')

urlpatterns = router.urls + course_router.urls
