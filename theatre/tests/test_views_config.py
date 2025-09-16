from rest_framework.permissions import IsAuthenticated, AllowAny
from theatre.views import (
    ActorViewSet, GenreViewSet, PlayViewSet, TheatreHallViewSet,
    PerformanceViewSet, ReservationViewSet, TicketViewSet,
    MeViewSet
)
from theatre.permissions import IsAdminOrReadOnly
from theatre.filters import PerformanceFilter
from theatre.serializers import PerformanceSerializer

def test_actor_genre_play_hall_are_readonly_for_anonymous():
    for vs in (ActorViewSet, GenreViewSet, PlayViewSet, TheatreHallViewSet, PerformanceViewSet):
        assert IsAdminOrReadOnly in vs.permission_classes

def test_reservation_and_ticket_require_auth():
    assert IsAuthenticated in ReservationViewSet.permission_classes
    assert IsAuthenticated in TicketViewSet.permission_classes

def test_me_view_requires_auth():
    assert IsAuthenticated in MeViewSet.permission_classes

def test_performance_viewset_filtering_and_ordering():
    assert PerformanceViewSet.filterset_class is PerformanceFilter
    assert PerformanceViewSet.ordering == ("show_time",)
