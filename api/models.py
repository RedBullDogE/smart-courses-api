from django.db import models


class Course(models.Model):
    """
    Model that represents course entity.
    """

    title = models.CharField(max_length=128)
    date_start = models.DateField()
    date_end = models.DateField()
    lecture_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title}"
