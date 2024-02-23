# from django.db import models

# from users.models import User
# from utils.models import BaseModel


# class Product(BaseModel):
#     owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="products")
#     name = models.CharField(max_length=256)

#     def __str__(self) -> str:
#         return f"{self.name} by {self.owner}"

#     class Meta:
#         verbose_name = "Product"
#         verbose_name_plural = "Products"


# class Lesson(BaseModel):
#     products = models.ManyToManyField(Product, related_name="lessons")
#     name = models.CharField(max_length=255)
#     video = models.FileField(upload_to="products/")
#     video_duration = models.PositiveIntegerField(default=0)

#     def __str__(self) -> str:
#         return f"{self.name} "

#     class Meta:
#         verbose_name = "Lesson"
#         verbose_name_plural = "Lessons"


# class Order(BaseModel):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
#     product = models.ForeignKey(
#         Product, on_delete=models.CASCADE, related_name="orders"
#     )

#     def __str__(self) -> str:
#         return f"{self.product} ordered by {self.owner}"

#     class Meta:
#         verbose_name = "Order"
#         verbose_name_plural = "Orders"


# class UserLesson(BaseModel):
#     owner = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="user_lessons"
#     )
#     lesson = models.ForeignKey(
#         Lesson, on_delete=models.CASCADE, related_name="user_lessons"
#     )
#     time_watched = models.PositiveIntegerField(default=0)
#     last_watched = models.DateTimeField(auto_now=True)
#     is_completed = models.BooleanField(default=False)

#     def __str__(self) -> str:
#         return f"{self.lesson} enrolled by {self.owner}"

#     @property
#     def check_complete(self):
#         if self.time_watched >= self.lesson.video_duration * 0.8:
#             self.is_completed = True
#         else:
#             self.is_completed = False
#         self.save()


# class UserLessonHistory(BaseModel):
#     # owner = models.ForeignKey(
#     #     User, on_delete=models.CASCADE, related_name="user_lesson_histories"
#     # )
#     # lesson = models.ForeignKey(
#     #     Lesson, on_delete=models.CASCADE, related_name="user_lesson_histories"
#     # )

#     user_lesson = models.ForeignKey(
#         UserLesson, on_delete=models.CASCADE, related_name="user_lesson_history"
#     )
#     watched_from = models.PositiveIntegerField(default=0)
#     watched_to = models.PositiveIntegerField(default=0)

#     def __str__(self) -> str:
#         return f"{self.user_lesson.lesson.name} watched by {self.user_lesson.owner.username} from {self.watched_from} to {self.watched_to}"


from django.db import models
from users.models import User

from utils.models import BaseModel


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.title}"


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self) -> str:
        return f"{self.product} ordered by {self.user}"


class Lesson(models.Model):
    product = models.ManyToManyField(Product, related_name="lessons")
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to="lessons/")
    duration_seconds = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.title}"


class LessonViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="lessons_viewed"
    )
    viewed_duration_seconds = models.IntegerField(default=0)
    is_complete = models.BooleanField(default=False)
    last_viewed = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.lesson.title} viewd by {self.user.username}"

    def save(self, *args, **kwargs):
        if self.viewed_duration_seconds >= 0.8 * self.lesson.duration_seconds:
            self.is_complete = True
        else:
            self.is_complete = False
        super().save(*args, **kwargs)
