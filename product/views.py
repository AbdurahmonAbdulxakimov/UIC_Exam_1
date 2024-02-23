# from django.db.models.query import QuerySet
# from django.db.models import F
# from rest_framework.generics import ListAPIView


# from product.models import Product, Lesson, Order, UserLesson, UserLessonHistory
# from product.serializers import (
#     ProductSerializer,
#     LessonSerializer,
#     OrderSerializer,
#     UserSerializer,
#     LessonByUser,
# )
# from users.models import User


# class LessonsByUserListAPIView(ListAPIView):
#     queryset = Lesson.objects.all().prefetch_related("products", "products__orders")
#     serializer_class = LessonByUser

#     def get_queryset(self) -> QuerySet:
#         user = self.request.user
#         # user = "admin"
#         qs = self.queryset.filter(products__orders__owner__id=user.id)
#         return qs.annotate(
#             time_watched=F("user_lessons__time_watched"),
#             is_complete=F("user_lessons__is_completed"),
#         )


# class LessonsByProductListAPIView(ListAPIView):

#     queryset = Lesson.objects.all().prefetch_related("products", "products__orders")
#     serializer_class = LessonByUser

#     def get_queryset(self):
#         product_id = self.kwargs.get("product_id")
#         qs = self.queryset.filter(
#             id=product_id,
#             products__orders__owner__id=self.request.user.id,
#         ).annotate(
#             time_watched=F("user_lessons__time_watched"),
#             is_complete=F("user_lessons__is_completed"),
#         )
#         return qs

from rest_framework import generics
from django.db.models import F

from .models import Lesson, LessonViewed
from .serializers import LessonSerializer, LessonViewSerializer


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        # Get all lessons associated with products the user has access to
        queryset = (
            Lesson.objects.prefetch_related("product", "lessons_viewed")
            .annotate(
                user=F("product__orders__user"),
                viewed_duration_seconds=F("lessons_viewed__viewed_duration_seconds"),
                is_complete=F("lessons_viewed__is_complete"),
            )
            .filter(product__orders__user=user)
        )
        return queryset

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context["user"] = self.request.user
    #     context["viewed_duration_seconds"] = None
    #     context["is_completed"] = None
    #     return context
