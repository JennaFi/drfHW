from django.urls import path
from rest_framework.routers import SimpleRouter

from courses.apps import CoursesConfig
from courses.views import CourseViewSet, LessonListAPIView, LessonRetrieveApiView, LessonUpdateApiView, \
    LessonDestroyApiView, LessonCreateApiView, SubscriptionAPIView, CoursePaymentCreateApiView

app_name = CoursesConfig.name

router = SimpleRouter()
router.register('courses/', CourseViewSet)

urlpatterns = [
    path('lessons', LessonListAPIView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>', LessonRetrieveApiView.as_view(), name='lesson_detail'),
    path('lessons/create', LessonCreateApiView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/update', LessonUpdateApiView.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete', LessonDestroyApiView.as_view(), name='lesson_delete'),
    path('subscriptions/<int:course_id>', SubscriptionAPIView.as_view(), name='subscription'),
    path('payment/', CoursePaymentCreateApiView.as_view(), name='payment'),

]

urlpatterns += router.urls
