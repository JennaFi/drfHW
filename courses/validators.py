from rest_framework.serializers import ValidationError

validator_url = 'youtube.com'

def validate_url(value):
    if not value in validator_url:
        raise ValidationError(f'{value} is not a valid YouTube URL.')