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
from django.db.models import F, Q, Count, Sum, ExpressionWrapper, FloatField

from .models import Lesson, LessonViewed, Product
from users.models import User
from .serializers import (
    LessonSerializer,
    LessonViewSerializer,
    ProductStatisticsSerializer,
)


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user

        if "product_id" in self.kwargs:
            product_id = self.kwargs.get("product_id")
            # Get all lessons of specific product associated with products the user has access to
            queryset = (
                Lesson.objects.prefetch_related(
                    "product", "lessons_viewed", "product__orders"
                )
                .annotate(
                    user=F("product__orders__user"),
                    viewed_duration_seconds=F(
                        "lessons_viewed__viewed_duration_seconds"
                    ),
                    is_complete=F("lessons_viewed__is_complete"),
                    last_viewed=F("lessons_viewed__last_viewed"),
                )
                .filter(Q(product__orders__user=user) & Q(product=product_id))
                .distinct()
            )
        else:
            # Get all lessons associated with products the user has access to
            queryset = (
                Lesson.objects.prefetch_related(
                    "product", "lessons_viewed", "product__orders"
                )
                .annotate(
                    user=F("product__orders__user"),
                    viewed_duration_seconds=F(
                        "lessons_viewed__viewed_duration_seconds"
                    ),
                    is_complete=F("lessons_viewed__is_complete"),
                    last_viewed=F("lessons_viewed__last_viewed"),
                )
                .filter(Q(product__orders__user=user))
                .distinct()
            )
        return queryset


class ProductStatisticsListAPIView(generics.ListAPIView):
    queryset = Product.objects.annotate(
        lessons_viewed_count=Count("lessons__lessons_viewed", distinct=True),
        total_viewed_duration_seconds=Sum(
            "lessons__lessons_viewed__viewed_duration_seconds"
        ),
        orders_count=Count("orders", distinct=True),
    ).annotate(
        percentage_orders=ExpressionWrapper(
            (F("orders_count") * 100.0) / User.objects.count(),
            output_field=FloatField(),
        )
    )
    serializer_class = ProductStatisticsSerializer
