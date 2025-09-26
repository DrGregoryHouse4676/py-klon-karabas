import pytest
from unittest.mock import patch

from django.utils import timezone

from theatre.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    PlayWriteSerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    TicketSerializer,
    ReservationSerializer,
    ReservationCreateSerializer,
    UserSerializer,
)


@pytest.mark.django_db
def test_actor_genre_serializers():
    actor = Actor.objects.create(first_name="Tom", last_name="Hanks")
    genre = Genre.objects.create(name="Drama")

    data = ActorSerializer(actor).data
    assert data["first_name"] == "Tom"
    assert data["last_name"] == "Hanks"

    gdata = GenreSerializer(genre).data
    assert gdata["name"] == "Drama"


@pytest.mark.django_db
def test_play_serializer_with_relations():
    actor = Actor.objects.create(first_name="Will", last_name="Smith")
    genre = Genre.objects.create(name="Comedy")
    play = Play.objects.create(title="Funny Play", description="test desc")
    play.actors.add(actor)
    play.genres.add(genre)

    data = PlaySerializer(play).data
    assert data["title"] == "Funny Play"
    assert data["actors"][0]["first_name"] == "Will"
    assert data["genres"][0]["name"] == "Comedy"


@pytest.mark.django_db
def test_play_write_serializer_create_and_update():
    actor = Actor.objects.create(first_name="A", last_name="B")
    genre = Genre.objects.create(name="Tragedy")

    # Create
    serializer = PlayWriteSerializer(
        data={
            "title": "Hamlet",
            "description": "desc",
            "actor_ids": [actor.id],
            "genre_ids": [genre.id],
        }
    )
    serializer.is_valid(raise_exception=True)
    play = serializer.save()
    assert play.actors.count() == 1
    assert play.genres.count() == 1

    # Update
    new_genre = Genre.objects.create(name="Classic")
    update_ser = PlayWriteSerializer(
        play, data={"genre_ids": [new_genre.id]}, partial=True
    )
    update_ser.is_valid(raise_exception=True)
    updated = update_ser.save()
    assert list(updated.genres.values_list("name", flat=True)) == ["Classic"]


@pytest.mark.django_db
def test_theatre_hall_serializer_capacity():
    hall = TheatreHall.objects.create(name="Main", rows=10, seats_in_row=20)
    data = TheatreHallSerializer(hall).data
    assert data["capacity"] == 200


@pytest.mark.django_db
@patch("theatre.serializers.build_seat_map")
def test_performance_serializer_with_seat_map(mock_build):
    play = Play.objects.create(title="Hamlet")
    hall = TheatreHall.objects.create(name="Hall", rows=5, seats_in_row=5)
    perf = Performance.objects.create(
        play=play, theatre_hall=hall, show_time=timezone.now()
    )
    mock_build.return_value = {"1": ["free", "free"]}

    data = PerformanceSerializer(perf).data
    assert "seat_map" in data
    assert data["seat_map"] == {"1": ["free", "free"]}
    mock_build.assert_called_once_with(perf)


@pytest.mark.django_db
def test_ticket_and_reservation_serializer(django_user_model):
    user = django_user_model.objects.create_user(username="u1", password="123")
    play = Play.objects.create(title="Play1")
    hall = TheatreHall.objects.create(name="Hall1", rows=3, seats_in_row=3)
    perf = Performance.objects.create(
        play=play, theatre_hall=hall, show_time=timezone.now()
    )
    res = Reservation.objects.create(user=user)
    ticket = Ticket.objects.create(performance=perf, reservation=res, row=1, seat=2)

    tdata = TicketSerializer(ticket).data
    assert tdata["row"] == 1
    assert tdata["seat"] == 2

    rdata = ReservationSerializer(res).data
    assert rdata["id"] == res.id
    assert rdata["tickets"][0]["row"] == 1


@pytest.mark.django_db
@patch("theatre.serializers.create_reservation")
def test_reservation_create_serializer(mock_create, rf, django_user_model):
    user = django_user_model.objects.create_user(username="u2", password="123")
    play = Play.objects.create(title="Play2")
    hall = TheatreHall.objects.create(name="Hall2", rows=3, seats_in_row=3)
    perf = Performance.objects.create(
        play=play, theatre_hall=hall, show_time=timezone.now()
    )

    mock_res = Reservation.objects.create(user=user)
    mock_create.return_value = mock_res

    request = rf.post("/reservations/")
    request.user = user
    serializer = ReservationCreateSerializer(
        data={"performance_id": perf.id, "seats": [{"row": 1, "seat": 1}]},
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    reservation = serializer.save()

    assert reservation == mock_res
    mock_create.assert_called_once_with(
        user=user, performance=perf, seats=[{"row": 1, "seat": 1}]
    )


@pytest.mark.django_db
def test_user_serializer(django_user_model):
    user = django_user_model.objects.create_user(username="lev", password="123")
    data = UserSerializer(user).data
    assert data["username"] == "lev"
