from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='Course Name')
    description = models.TextField(blank=True, null=True, verbose_name='Course Description')
    preview = models.ImageField(upload_to='courses/preview/%Y/%m/%d', blank=True, null=True,
                                verbose_name='Course Preview')

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

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['course']

    def __str__(self):
        return self.name + ' ' + self.course
