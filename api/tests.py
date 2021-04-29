from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course


class CourseTest(APITestCase):
    def test_create_course(self):
        url = reverse("course-list")
        data = {
            "title": "New Test Course",
            "date_start": "2021-05-01",
            "date_end": "2021-06-01",
            "lecture_number": "12",
        }

        response = self.client.post(url, data, format="json")

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Course.objects.all().count(), 1)
        self.assertEquals(Course.objects.get().title, "New Test Course")
