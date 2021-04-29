from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from api.serializers import CourseDetailsSerializer, CourseShortSerializer

from .models import Course


class CourseViewSet(ModelViewSet):
    """
    Set of CRUD views for Course model. Also provides searching by title field
    and date filter (supports both exact matches and date ranges).
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
