from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from .models import Actor, Genre, Play, TheatreHall, Performance, Reservation, Ticket
from .serializers import (
    ActorSerializer, GenreSerializer, PlaySerializer, PlayWriteSerializer,
    TheatreHallSerializer, PerformanceSerializer,
    ReservationSerializer, ReservationCreateSerializer,
    TicketSerializer, UserSerializer,
    )
from .permissions import IsAdminOrReadOnly
from .filters import PerformanceFilter


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("first_name", "last_name")


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("name",)


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("actors", "genres")
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return PlayWriteSerializer
        return PlaySerializer

    search_fields = ("title", "actors__first_name", "actors__last_name", "genres__name")


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("name",)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("play", "theatre_hall")
    serializer_class = PerformanceSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = PerformanceFilter
    ordering = ("show_time",)


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).prefetch_related("tickets__performance__play","tickets__performance__theatre_hall")

    def get_serializer_class(self):
        if self.action == "create":
            return ReservationCreateSerializer
        return ReservationSerializer


class TicketViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Ticket.objects.filter(reservation__user=self.request.user).select_related(
"performance__play", "performance__theatre_hall", "reservation"
)

    serializer_class = TicketSerializer


class MeViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
