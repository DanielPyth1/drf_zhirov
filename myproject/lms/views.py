from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModerator, IsOwner
from .paginators import CourseLessonPagination
from .models import Payment
from .services import create_product, create_price, create_checkout_session
from django.http import HttpResponse

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CourseLessonPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CourseLessonPagination

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course)

        if not created:
            subscription.delete()
            return Response({"message": "Подписка удалена"}, status=status.HTTP_200_OK)

        return Response({"message": "Подписка добавлена"}, status=status.HTTP_201_CREATED)


class CreatePaymentView(APIView):
    def post(self, request):
        course_id = request.data.get("course_id")
        course = Course.objects.get(id=course_id)

        product = create_product(course.title)
        price = create_price(product.id, int(course.price * 100))  # в копейках
        session = create_checkout_session(
            price.id,
            "http://127.0.0.1:8000/success/",
            "http://127.0.0.1:8000/cancel/",
        )

        payment = Payment.objects.create(
            course=course,
            price_id=price.id,
            session_id=session.id,
            checkout_url=session.url,
        )

        return Response({"checkout_url": payment.checkout_url})


def payment_success(request):
    return HttpResponse("Оплата прошла успешно!")

def payment_cancel(request):
    return HttpResponse("Оплата была отменена.")