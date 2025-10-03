import pytest
from unittest.mock import MagicMock, patch
from users.models import User, UserManager


@pytest.fixture
def user_manager():
    mgr = UserManager()
    mgr.model = User
    return mgr


def test_create_user_without_email_raises(user_manager):
    with pytest.raises(ValueError, match="The Email field must be set"):
        user_manager.create_user(email=None, password="123")


@patch.object(User, "save", MagicMock())
@patch.object(User, "set_password", MagicMock())
def test_create_user_sets_email_and_password(user_manager):
    user = user_manager.create_user("test@example.com", "pass123")

    assert isinstance(user, User)
    assert user.email == "test@example.com"
    user.set_password.assert_called_once_with("pass123")
    user.save.assert_called_once()


@patch.object(User, "save", MagicMock())
@patch.object(User, "set_password", MagicMock())
def test_create_superuser_sets_staff_and_superuser(user_manager):
    user = user_manager.create_superuser("admin@example.com", "adminpass")

    assert user.is_staff is True
    assert user.is_superuser is True


def test_create_superuser_with_invalid_flags_raises(user_manager):
    with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
        user_manager.create_superuser("x@y.com", "123", is_staff=False)

    with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
        user_manager.create_superuser("x@y.com", "123", is_superuser=False)


def test_user_str_returns_email():
    user = User(email="user@example.com")
    assert str(user) == "user@example.com"
