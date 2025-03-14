from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics

from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Lesson, Subscription
from courses.pagination import CustomPagination
from courses.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer, CoursePaymentSerializer
from courses.services import create_stipe_price, create_stripe_session
from users.permissions import IsModerator, IsUser, IsOwner
from .tasks import send_mail_course_update


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModerator, IsUser)
        elif self.action == 'destroy':
            self.permission_classes = (~IsModerator | IsOwner,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModerator | IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        course_id = self.kwargs.get('pk')
        send_mail_course_update.delay(course_id)


class LessonCreateApiView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    permission_classes = (~IsModerator, IsUser)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator, IsUser | IsOwner)
    pagination_class = CustomPagination


class LessonRetrieveApiView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator, IsUser | IsOwner)


class LessonDestroyApiView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsUser, IsOwner, ~IsModerator)


class LessonUpdateApiView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator, IsUser | IsOwner)


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = (IsUser,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = request.data.get('course')
        course = get_object_or_404(Course, pk=course_id)
        subs_item = self.queryset.filter(course=course, user=user)

        if subs_item.exists():
            subs_item.delete()
            message = 'Subscription deleted'
        else:
            Subscription.objects.create(course=course, user=user)
            message = 'Subscription renewed'
        return Response(message)


class CoursePaymentCreateApiView(generics.CreateAPIView):
    serializer_class = CoursePaymentSerializer
    permission_classes = [IsUser]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        course_id = self.request.data.get('course')
        course = get_object_or_404(Course, id=course_id)
        amount_in_usd = course.price
        payment = serializer.save(amount=amount_in_usd)
        price = create_stipe_price(amount_in_usd, course.name)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
