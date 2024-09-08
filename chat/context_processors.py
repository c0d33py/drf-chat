from __future__ import annotations

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest

User = get_user_model()


def debug(request: HttpRequest) -> dict[str, str]:
    return {"DEBUG": settings.DEBUG}


def users(request):
    queryset = User.objects.all().order_by('username')
    return {'users': queryset}
