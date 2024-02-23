from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from users.api.views import UserViewSet
from product.views import LessonListView, ProductStatisticsListAPIView


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
    path("lessons/<int:product_id>/", LessonListView.as_view(), name="lesson-list"),
    path(
        "products/statistics/",
        ProductStatisticsListAPIView.as_view(),
        name="product-statistics",
    ),
]
urlpatterns += router.urls
