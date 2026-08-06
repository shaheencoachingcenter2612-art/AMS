from django.db import models


class Session(models.Model):
    name = models.CharField(max_length=50)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=20)
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name="sections"
    )

    def __str__(self):
        return f"{self.classroom.name} - {self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name