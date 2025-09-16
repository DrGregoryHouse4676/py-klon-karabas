import pytest
from datetime import datetime, timedelta, timezone

from theatre.models import Play, TheatreHall, Performance
from theatre.filters import PerformanceFilter


@pytest.fixture
def sample_data(db):
    """Створюємо тестові дані: 2 вистави у різні дати і в різних залах."""
    play1 = Play.objects.create(title="Hamlet")
    play2 = Play.objects.create(title="Macbeth")
    hall1 = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
    hall2 = TheatreHall.objects.create(name="Small Hall", rows=5, seats_in_row=10)

    now = datetime.now(timezone.utc)
    perf1 = Performance.objects.create(
        play=play1,
        theatre_hall=hall1,
        show_time=now + timedelta(days=1),
    )
    perf2 = Performance.objects.create(
        play=play2,
        theatre_hall=hall2,
        show_time=now + timedelta(days=7),
    )
    return {"play1": play1, "play2": play2, "hall1": hall1, "hall2": hall2, "perf1": perf1, "perf2": perf2, "now": now}


@pytest.mark.django_db
def test_filter_date_from(sample_data):
    f = PerformanceFilter(
        {"date_from": (sample_data["now"] + timedelta(days=3)).isoformat()},
        queryset=Performance.objects.all(),
    )
    qs = f.qs
    assert sample_data["perf1"] not in qs
    assert sample_data["perf2"] in qs


@pytest.mark.django_db
def test_filter_date_to(sample_data):
    f = PerformanceFilter(
        {"date_to": (sample_data["now"] + timedelta(days=3)).isoformat()},
        queryset=Performance.objects.all(),
    )
    qs = f.qs
    assert sample_data["perf1"] in qs
    assert sample_data["perf2"] not in qs


@pytest.mark.django_db
def test_filter_by_play_title(sample_data):
    f = PerformanceFilter(
        {"play": "hamlet"},
        queryset=Performance.objects.all(),
    )
    qs = f.qs
    assert sample_data["perf1"] in qs
    assert sample_data["perf2"] not in qs


@pytest.mark.django_db
def test_filter_by_hall_name(sample_data):
    f = PerformanceFilter(
        {"hall": "small"},
        queryset=Performance.objects.all(),
    )
    qs = f.qs
    assert sample_data["perf1"] not in qs
    assert sample_data["perf2"] in qs
