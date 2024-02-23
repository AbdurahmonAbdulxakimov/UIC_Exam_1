from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from users.api.views import UserViewSet
from product.views import LessonListView


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = [
    # path("lessons/", LessonsByUserListAPIView.as_view()),
    # path("products/<int:product_id>/lessons/", LessonsByProductListAPIView.as_view()),
    path("lessons/", LessonListView.as_view(), name="lesson-list"),
]
urlpatterns += router.urls
