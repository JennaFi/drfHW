from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config.settings import DEFAULT_FROM_EMAIL
from courses.models import Course


@shared_task
def send_mail_course_update(course_id):
    course = get_object_or_404(Course, id=course_id)
    subscriptions = course.subscription.all()
    recipient_list = [sub.user.email for sub in subscriptions]
    subject = f'{course.name} renewed'
    message = f'There are changes in "{course.name}" '

    from_email = DEFAULT_FROM_EMAIL

    responses = {}

    for recipient in recipient_list:
        try:
            send_mail(subject, message, from_email, [recipient])

            responses[recipient] = 'Success'
        except Exception as e:
            response = f'{recipient}: Error: {str(e)}'
            responses[recipient] = f'Error: {str(e)}'

    print(responses)
