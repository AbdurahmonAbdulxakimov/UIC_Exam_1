# from rest_framework import serializers

# from product.models import Product, Lesson, Order, UserLesson, UserLessonHistory
# from users.models import User


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("id", "username")


# class ProductSerializer(serializers.ModelSerializer):
#     owner = UserSerializer()

#     class Meta:
#         model = Product
#         fields = ("id", "name", "owner")


# class LessonSerializer(serializers.ModelSerializer):
#     products = ProductSerializer(many=True)

#     class Meta:
#         model = Lesson
#         fields = ("id", "name", "video", "video_duration", "products")


# class OrderSerializer(serializers.ModelSerializer):
#     owner = UserSerializer()
#     product = ProductSerializer()

#     class Meta:
#         model = Order
#         fields = ("id", "owner", "product")


# class UserLessonSerializer(serializers.ModelSerializer):
#     owner = UserSerializer()
#     lesson = LessonSerializer()

#     class Meta:
#         model = UserLesson
#         fields = ("id", "owner", "lesson", "time_watched", "is_completed")


# class LessonByUser(serializers.ModelSerializer):
#     product = ProductSerializer(many=True, read_only=True)

#     class Meta:
#         model = Lesson
#         fields = (
#             "id",
#             "name",
#             "video",
#             "video_duration",
#             "product",
#             "is_completed",
#             "time_watched",
#         )


from rest_framework import serializers
from .models import Lesson, LessonViewed, Product
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class ProductSerializer(serializers.ModelSerializer):
    # owner = UserSerializer()

    class Meta:
        model = Product
        fields = ("id", "title", "owner")


class LessonSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = (
            "id",
            "product",
            "title",
            "video",
            "duration_seconds",
            "created_at",
            "updated_at",
        )


class LessonViewedSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer()
    user = UserSerializer()

    class Meta:
        model = LessonViewed
        fields = (
            "id",
            "user",
            "lesson",
            "viewed_duration_seconds",
            "is_complete",
            "last_viewed",
        )


class ProductStatisticsSerializer(serializers.ModelSerializer):
    lessons_viewed = LessonViewedSerializer(many=True, read_only=True)
    lessons_viewed_count = serializers.IntegerField()
    total_viewed_duration_seconds = serializers.IntegerField()
    percentage_orders = serializers.FloatField()

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "lessons_viewed",
            "lessons_viewed_count",
            "total_viewed_duration_seconds",
            "percentage_orders",
        )
