import pytest
from django.contrib import admin
from django.urls import reverse
from django.test import Client

from theatre.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)
from theatre.admin import (
    ActorAdmin,
    GenreAdmin,
    PlayAdmin,
    TheatreHallAdmin,
    PerformanceAdmin,
    ReservationAdmin,
    TicketAdmin,
)


@pytest.mark.django_db
def test_admin_registration():
    site = admin.site
    assert Actor in site._registry
    assert Genre in site._registry
    assert Play in site._registry
    assert TheatreHall in site._registry
    assert Performance in site._registry
    assert Reservation in site._registry
    assert Ticket in site._registry


@pytest.mark.django_db
def test_actor_admin_list_display():
    admin_instance = ActorAdmin(Actor, admin.site)
    assert "first_name" in admin_instance.list_display
    assert "last_name" in admin_instance.list_display
    assert "first_name" in admin_instance.search_fields


@pytest.mark.django_db
def test_genre_admin_list_display():
    admin_instance = GenreAdmin(Genre, admin.site)
    assert "name" in admin_instance.list_display
    assert "name" in admin_instance.search_fields


@pytest.mark.django_db
def test_play_admin_fields():
    admin_instance = PlayAdmin(Play, admin.site)
    assert "title" in admin_instance.list_display
    assert "title" in admin_instance.search_fields
    assert "actors" in admin_instance.filter_horizontal
    assert "genres" in admin_instance.filter_horizontal


@pytest.mark.django_db
def test_theatre_hall_admin_list_display():
    admin_instance = TheatreHallAdmin(TheatreHall, admin.site)
    assert "capacity" in admin_instance.list_display


@pytest.mark.django_db
def test_performance_admin_list_display_and_filter():
    admin_instance = PerformanceAdmin(Performance, admin.site)
    assert "play" in admin_instance.list_display
    assert "theatre_hall" in admin_instance.list_display
    assert "show_time" in admin_instance.list_display
    assert "theatre_hall" in admin_instance.list_filter
    assert "show_time" in admin_instance.list_filter


@pytest.mark.django_db
def test_reservation_admin_inline_tickets():
    admin_instance = ReservationAdmin(Reservation, admin.site)
    assert any(inline.model is Ticket for inline in admin_instance.inlines)


@pytest.mark.django_db
def test_ticket_admin_list_display_and_search():
    admin_instance = TicketAdmin(Ticket, admin.site)
    assert "performance" in admin_instance.list_display
    assert "row" in admin_instance.list_display
    assert "seat" in admin_instance.list_display
    assert "reservation" in admin_instance.list_display
    assert "performance__play__title" in admin_instance.search_fields


@pytest.mark.django_db
def test_admin_pages_accessible(admin_client: Client):
    urls = [
        reverse("admin:theatre_actor_changelist"),
        reverse("admin:theatre_genre_changelist"),
        reverse("admin:theatre_play_changelist"),
        reverse("admin:theatre_theatrehall_changelist"),
        reverse("admin:theatre_performance_changelist"),
        reverse("admin:theatre_reservation_changelist"),
        reverse("admin:theatre_ticket_changelist"),
    ]
    for url in urls:
        response = admin_client.get(url)
        assert response.status_code == 200
