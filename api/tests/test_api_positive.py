from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Course


class CourseAPIPositiveTests(APITestCase):
    """
    Testing positive cases for Course API.
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

    def test_create_course(self):
        # GIVEN
        url = reverse("course-list")
        data = {
            "title": "New Test Course",
            "date_start": "2021-05-01",
            "date_end": "2021-06-01",
            "lecture_number": "12",
        }

        # WHEN
        response = self.client.post(url, data, format="json")

        # THEN
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Course.objects.all().count(), 4)
        self.assertEquals(Course.objects.last().title, "New Test Course")

    def test_list_courses(self):
        # GIVEN
        url = reverse("course-list")

        # WHEN
        response = self.client.get(url)
        response_body = response.json()

        # THEN
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response_body["count"], 3)

    def test_retrieve_course(self):
        # GIVEN
        url = reverse("course-detail", args=[self.courses[0].id])

        # WHEN
        response = self.client.get(url)
        response_body = response.json()

        # THEN
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response_body["title"], "Test Title 1")
        self.assertEquals(response_body["date_start"], "2021-06-01")
        self.assertEquals(response_body["date_end"], "2021-06-08")
        self.assertEquals(response_body["lecture_number"], 3)

    def test_update_course(self):
        # GIVEN
        url = reverse("course-detail", args=[self.courses[1].id])
        data = {
            "title": "Changed Title",
            "date_start": "2025-06-01",
            "date_end": "2025-06-08",
            "lecture_number": 20,
        }

        # WHEN
        response = self.client.put(url, data=data, format="json")
        response_body = response.json()

        # THEN
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response_body["title"], "Changed Title")
        self.assertEquals(response_body["date_start"], "2025-06-01")
        self.assertEquals(response_body["date_end"], "2025-06-08")
        self.assertEquals(response_body["lecture_number"], 20)

    def test_delete_course(self):
        # GIVEN
        url = reverse("course-detail", args=[self.courses[2].id])

        # WHEN
        response = self.client.delete(url)

        # THEN
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Course.objects.all().count(), 2)

    def test_search_courses_by_title(self):
        # GIVEN
        url = reverse("course-list")
        search_url1 = f"{url}?search=test title"
        search_url2 = f"{url}?search=cool"
        search_url3 = f"{url}?search=test title 2"

        # WHEN
        response1 = self.client.get(search_url1)
        response1_body = response1.json()

        response2 = self.client.get(search_url2)
        response2_body = response2.json()

        response3 = self.client.get(search_url3)
        response3_body = response3.json()

        # THEN
        self.assertEquals(response1.status_code, status.HTTP_200_OK)
        self.assertEquals(response1_body["count"], 3)

        self.assertEquals(response2.status_code, status.HTTP_200_OK)
        self.assertEquals(response2_body["count"], 1)

        self.assertEquals(response3.status_code, status.HTTP_200_OK)
        self.assertEquals(response3_body["count"], 1)

    def test_filter_courses_by_date(self):
        # GIVEN
        url = reverse("course-list")
        filter_url1 = f"{url}?date_start=2021-06-01"  # first course
        filter_url2 = f"{url}?date_start__gte=2021-06-14"  # second and third courses

        filter_url3 = f"{url}?date_end__lte=2021-12-01"  # all courses
        filter_url4 = f"{url}?date_end=2021-06-08"  # only first course

        # only second course
        filter_url5 = f"{url}?date_start__gte=2021-06-14&date_end__lte=2021-07-01"

        # WHEN
        response1 = self.client.get(filter_url1)
        response1_body = response1.json()

        response2 = self.client.get(filter_url2)
        response2_body = response2.json()

        response3 = self.client.get(filter_url3)
        response3_body = response3.json()

        response4 = self.client.get(filter_url4)
        response4_body = response4.json()

        response5 = self.client.get(filter_url5)
        response5_body = response5.json()

        # THEN
        self.assertEquals(response1.status_code, status.HTTP_200_OK)
        self.assertEquals(response1_body["count"], 1)

        self.assertEquals(response2.status_code, status.HTTP_200_OK)
        self.assertEquals(response2_body["count"], 2)

        self.assertEquals(response3.status_code, status.HTTP_200_OK)
        self.assertEquals(response3_body["count"], 3)

        self.assertEquals(response4.status_code, status.HTTP_200_OK)
        self.assertEquals(response4_body["count"], 1)

        self.assertEquals(response5.status_code, status.HTTP_200_OK)
        self.assertEquals(response5_body["count"], 1)
