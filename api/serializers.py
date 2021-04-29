from rest_framework import serializers

from .models import Course


class CourseShortSerializer(serializers.ModelSerializer):
    """
    Course serializer class, provided for short representation of course
    entities. May be used in lists.
    """

    class Meta:
        model = Course
        fields = ["id", "title", "date_start", "date_end"]


class CourseDetailsSerializer(serializers.ModelSerializer):
    """
    Course serializer class, provided for detailed representation of course
    entities. May be used for detail pages, create or update forms etc.
    """

    class Meta:
        model = Course
        fields = "__all__"

    def validate(self, attrs):

        if attrs["date_start"] > attrs["date_end"]:
            raise serializers.ValidationError(
                {"date_end": "date_end should be after date_start"}
            )

        if attrs["lecture_number"] < 0:
            raise serializers.ValidationError(
                {"lecture_number": "value must be positive"}
            )
        return attrs
