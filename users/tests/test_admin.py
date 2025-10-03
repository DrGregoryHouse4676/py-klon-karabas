import pytest
from django.contrib import admin

from users.admin import UserAdmin
from users.models import User


@pytest.fixture
def user_admin():
    return UserAdmin(User, admin.site)


def test_ordering_is_by_email(user_admin):
    assert user_admin.ordering == ("email",)


def test_list_display_contains_expected_fields(user_admin):
    assert "email" in user_admin.list_display
    assert "is_staff" in user_admin.list_display
    assert "is_active" in user_admin.list_display


def test_search_fields(user_admin):
    assert user_admin.search_fields == ("email",)


def test_fieldsets_have_expected_structure(user_admin):
    fieldsets = dict(user_admin.fieldsets)
    assert None in fieldsets
    assert "Permissions" in fieldsets
    assert "Important dates" in fieldsets
    assert "email" in fieldsets[None]["fields"]
    assert "password" in fieldsets[None]["fields"]


def test_add_fieldsets_have_expected_fields(user_admin):
    add_fieldsets = dict(user_admin.add_fieldsets)
    fields = add_fieldsets[None]["fields"]
    for f in ("email", "password1", "password2", "is_active", "is_staff"):
        assert f in fields
