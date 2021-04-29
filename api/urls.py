from rest_framework.routers import DefaultRouter

from api.views import CourseViewSet

router = DefaultRouter()

router.register("courses", CourseViewSet, basename="course")

urlpatterns = router.urls
