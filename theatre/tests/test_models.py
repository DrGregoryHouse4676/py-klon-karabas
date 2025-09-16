import pytest
from django.db import IntegrityError
from django.utils import timezone

from theatre.models import Actor, Genre, Play, TheatreHall, Performance, Reservation, Ticket


@pytest.mark.django_db
def test_actor_str():
    actor = Actor.objects.create(first_name="William", last_name="Shakespeare")
    assert str(actor) == "William Shakespeare"


@pytest.mark.django_db
def test_genre_str():
    genre = Genre.objects.create(name="Drama")
    assert str(genre) == "Drama"


@pytest.mark.django_db
def test_play_str_and_relations():
    actor = Actor.objects.create(first_name="Tom", last_name="Hanks")
    genre = Genre.objects.create(name="Comedy")
    play = Play.objects.create(title="Funny Play")
    play.actors.add(actor)
    play.genres.add(genre)

    assert str(play) == "Funny Play"
    assert actor in play.actors.all()
    assert genre in play.genres.all()


@pytest.mark.django_db
def test_theatre_hall_capacity_and_str():
    hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
    assert hall.capacity == 200
    assert str(hall) == "Main Hall (10x20)"


@pytest.mark.django_db
def test_performance_str_and_unique_constraint():
    play = Play.objects.create(title="Hamlet")
    hall = TheatreHall.objects.create(name="Hall A", rows=5, seats_in_row=5)
    show_time = timezone.now()

    perf1 = Performance.objects.create(play=play, theatre_hall=hall, show_time=show_time)
    assert str(perf1).startswith("Hamlet @ Hall A")

    with pytest.raises(IntegrityError):
        Performance.objects.create(play=play, theatre_hall=hall, show_time=show_time)


@pytest.mark.django_db
def test_reservation_str_and_ordering(django_user_model):
    user = django_user_model.objects.create_user(username="testuser", password="12345")
    res = Reservation.objects.create(user=user)
    assert str(res) == f"Reservation #{res.pk} by {user}"
    assert Reservation.objects.first() == res  # ordering -created_at



