from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='Course Name')
    description = models.TextField(blank=True, null=True, verbose_name='Course Description')
    preview = models.ImageField(upload_to='courses/preview/%Y/%m/%d', blank=True, null=True,
                                verbose_name='Course Preview')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='courses', verbose_name='owner',
                              blank=True,
                              null=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['name']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name='Lesson Name')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Course')
    description = models.TextField(blank=True, null=True, verbose_name='Lesson Description')
    video_url = models.URLField(blank=True, null=True, verbose_name='Video URL')
    preview = models.ImageField(upload_to='lessons/preview/%Y/%m/%d', blank=True, null=True,
                                verbose_name='Lesson Preview')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='lessons', verbose_name='owner',
                              blank=True,
                              null=True)

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['course']

    def __str__(self):
        return self.name + ' ' + self.course


class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='courses_subscription',
                             verbose_name='User')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Course')

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        unique_together = ('user', 'course')

    def __str__(self):
        return self.user.username + '->' + self.course.name


class CoursePayment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_payments', verbose_name='Course')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True,
                             related_name='course_payments', verbose_name='User')
    amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='Amount')
    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID session')
    link = models.URLField(max_length=400, blank=True, null=True, verbose_name='Hyperlink to payment')

    class Meta:
        verbose_name = 'Course Payment'
        verbose_name_plural = 'Course Payments'
        ordering = ['-course']

    def __str__(self):
        return self.course.name + ' ' + self.amount + ' ' + self.user
