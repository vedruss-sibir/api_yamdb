from django.core.exceptions import ValidationError
from django.utils import timezone


def year_of_creation_validator(value):
    if not (0 < value <= timezone.now().year):
        raise ValidationError('Год произведения не может быть из будущего')
