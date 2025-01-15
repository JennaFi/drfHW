from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='Course Name')
    description = models.TextField(blank=True, null=True, verbose_name='Course Description')
    preview = models.ImageField(upload_to='courses/preview/%Y/%m/%d', blank=True, null=True, verbose_name='Course Preview')

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

        def __str__(self):
            return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name='Lesson Name')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Course')

