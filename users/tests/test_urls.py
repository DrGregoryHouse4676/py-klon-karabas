import pytest
from django.urls import reverse, resolve
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


@pytest.mark.parametrize(
    "url_name,view_class",
    [
        ("token_obtain_pair", TokenObtainPairView),
        ("token_refresh", TokenRefreshView),
        ("token_verify", TokenVerifyView),
    ],
)
def test_jwt_urls_resolve_to_correct_views(url_name, view_class):
    url = reverse(url_name)
    resolver = resolve(url)
    assert resolver.func.view_class == view_class
