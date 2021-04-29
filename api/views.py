from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from api.serializers import CourseDetailsSerializer, CourseShortSerializer

from .models import Course


class CourseViewSet(ModelViewSet):
    """
    Set of CRUD views for Course model. Also provides searching by title field
    and date filter (supports both exact matches and date ranges).

    create: Add a new course with specified fields (title, start date, end date and number of lectures).

    list: Get paginated list of existing courses. Allows us to search courses by title and filter by date.

    retrieve: Get detailed information about specific course.

    update: Update course information (replace the whole entity with a new one).

    partial_update: Update course fields (change only specified fields).

    destroy: Delete a course by its id.
    """

    queryset = Course.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["title"]
    filterset_fields = {
        "date_start": ["gte", "lte", "exact"],
        "date_end": ["gte", "lte", "exact"],
    }

    def get_serializer_class(self):
        if self.action == "list":
            return CourseShortSerializer

        return CourseDetailsSerializer
