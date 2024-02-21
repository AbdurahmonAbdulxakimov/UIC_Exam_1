from django.db import models

from users.models import User
from utils.models import BaseModel


class Product(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f"{self.name} by {self.owner}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Lesson(BaseModel):
    product = models.ManyToManyField(Product, related_name="courses")
    name = models.CharField(max_length=255)
    video = models.FileField(upload_to="products/")
    video_duration = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.name} by {self.owner}"

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"


class Order(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self) -> str:
        return f"{self.product} ordered by {self.owner}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class UserLessonHistory(BaseModel):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_lesson_histories"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="user_lesson_histories"
    )
    watched_from = models.PositiveIntegerField(default=0)
    watched_to = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.lesson} watched by {self.owner} from {self.watched_from} to {self.watched_to}"


class UserLesson(BaseModel):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_lessons"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="user_lessons"
    )
    time_watched = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.lesson} enrolled by {self.owner}"

    @property
    def check_complete(self):
        if self.time_watched >= self.lesson.video_duration * 0.8:
            self.is_completed = True
        else:
            self.is_completed = False
        self.save()
