import pytest
from datetime import date, time, timedelta
from django.contrib.auth.models import User
from theatre.models import TheatreHall, Play, Performance

@pytest.fixture
def user(db):
    return User.objects.create_user(username="lev", password="pass")

@pytest.fixture
def hall(db):
    return TheatreHall.objects.create(name="Big scena", rows=3, seats_in_row=4)

@pytest.fixture
def play(db):
    return Play.objects.create(title="Hamlet", description="...")

@pytest.fixture
def performance(db, hall, play):
    return Performance.objects.create(
        play=play,
        show_time=time(19, 0),
        show_date=date.today() + timedelta(days=1),
        hall=hall,
    )

# DRF клієнт, якщо потрібен у тестах API
from rest_framework.test import APIClient  # noqa: E402
@pytest.fixture
def api_client():
    return APIClient()
