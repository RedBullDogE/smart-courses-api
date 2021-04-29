from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Course


class CourseAPINegativeTests(APITestCase):
    """
    Testing negative cases for Course API.
    """

    @classmethod
    def setUpTestData(cls):
        cls.courses = [
            Course.objects.create(
                title="Test Title 1",
                date_start="2021-06-01",
                date_end="2021-06-08",
                lecture_number=3,
            ),
            Course.objects.create(
                title="Test Title 2",
                date_start="2021-06-14",
                date_end="2021-07-01",
                lecture_number=6,
            ),
            Course.objects.create(
                title="Cool Test Title 3",
                date_start="2021-09-06",
                date_end="2021-11-06",
                lecture_number=9,
            ),
        ]

    def test_create_course_with_wrong_date(self):
        # GIVEN
        url = reverse("course-list")
        data = {
            "title": "New Test Course",
            "date_start": "2021-05-01",
            "date_end": "2021-04-01",
            "lecture_number": "12",
        }

        # WHEN
        response = self.client.post(url, data, format="json")

        # THEN
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Course.objects.all().count(), 3)

    def test_retrieve_nonexistent_course(self):
        # GIVEN
        url = reverse("course-detail", args=[999])

        # WHEN
        response = self.client.get(url)

        # THEN
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_course_with_wrong_date(self):
        # GIVEN
        url = reverse("course-detail", args=[self.courses[1].id])
        data = {
            "title": "Changed Title",
            "date_start": "2025-06-01",
            "date_end": "2025-01-01",
            "lecture_number": 20,
        }

        # WHEN
        response = self.client.put(url, data=data, format="json")

        # THEN
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_nonexistent_course(self):
        # GIVEN
        url = reverse("course-detail", args=[999])
        data = {
            "title": "Some New Title",
            "date_start": "2025-06-01",
            "date_end": "2025-06-10",
            "lecture_number": 5,
        }

        # WHEN
        response = self.client.put(url, data=data, format="json")

        # THEN
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_course(self):
        # GIVEN
        url = reverse("course-detail", args=[999])

        # WHEN
        response = self.client.delete(url)

        # THEN
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(Course.objects.all().count(), 3)

    def test_filter_courses_with_wrong_query_data(self):
        # GIVEN
        url = reverse("course-list")
        wrong_url1 = f"{url}?date_start=202"  # first course
        wrong_url2 = f"{url}?date_end__gte=asd"  # second and third courses

        # WHEN
        response1 = self.client.get(wrong_url1)

        response2 = self.client.get(wrong_url2)

        # THEN
        self.assertEquals(response1.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEquals(response2.status_code, status.HTTP_400_BAD_REQUEST)
