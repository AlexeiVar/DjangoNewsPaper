import pytz
from django.utils import timezone


def timezones(request):
    return {'timezones': pytz.common_timezones, 'current_time': timezone.now()}
