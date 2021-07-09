import typing
from django.http import HttpRequest
from rest_framework import permissions
from django.conf import settings


class KeyParser:
    def get(self, request: HttpRequest) -> typing.Optional[str]:
        header = getattr(settings, "X_API_KEY_HEADER", None)
        if header is not None:
            return self.get_from_header(request, header)
        return ""

    def get_from_header(self, request: HttpRequest, name: str) -> typing.Optional[str]:
        return request.META.get(name) or None


class HasXAPIKey(permissions.BasePermission):
    key_parser = KeyParser()

    def get_key(self, request: HttpRequest) -> typing.Optional[str]:
        return self.key_parser.get(request)

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:
        API_KEY = getattr(settings, "API_KEY", None)
        assert API_KEY, "API-KEY is not set in settings"
        key = self.get_key(request)
        if not key:
            return False
        return key == API_KEY
