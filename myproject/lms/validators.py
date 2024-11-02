

from django.core.exceptions import ValidationError
import re

def youtube_link_validator(link):
    if not link:
        return
    if not re.match(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.*$', link):
        raise ValidationError('Only YouTube links are allowed.')
