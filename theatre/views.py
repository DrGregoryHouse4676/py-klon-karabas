from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)

from .filters import PerformanceFilter
from .models import Actor, Genre, Play, TheatreHall, Performance, Reservation, Ticket
from .permissions import IsAdminOrReadOnly
from .serializers import (
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    PlayWriteSerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    ReservationCreateSerializer,
    ReservationSerializer,
    TicketSerializer,
    UserSerializer,
)

User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        summary="List actors",
        tags=["Actors"],
        responses={200: ActorSerializer(many=True)},
    ),
    retrieve=extend_schema(summary="Retrieve actor", tags=["Actors"]),
    create=extend_schema(summary="Create actor", tags=["Actors"]),
    update=extend_schema(summary="Update actor", tags=["Actors"]),
    partial_update=extend_schema(summary="Partially update actor", tags=["Actors"]),
    destroy=extend_schema(summary="Delete actor", tags=["Actors"]),
)
class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("first_name", "last_name")


@extend_schema_view(
    list=extend_schema(
        summary="List genres",
        tags=["Genres"],
        responses={200: GenreSerializer(many=True)},
    ),
    retrieve=extend_schema(summary="Retrieve genre", tags=["Genres"]),
    create=extend_schema(summary="Create genre", tags=["Genres"]),
    update=extend_schema(summary="Update genre", tags=["Genres"]),
    partial_update=extend_schema(summary="Partially update genre", tags=["Genres"]),
    destroy=extend_schema(summary="Delete genre", tags=["Genres"]),
)
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("name",)


@extend_schema_view(
    list=extend_schema(
        summary="List plays", tags=["Plays"], responses={200: PlaySerializer(many=True)}
    ),
    retrieve=extend_schema(summary="Retrieve play", tags=["Plays"]),
    create=extend_schema(
        summary="Create play",
        tags=["Plays"],
        request=PlayWriteSerializer,
        responses={201: PlaySerializer},
    ),
    update=extend_schema(
        summary="Update play",
        tags=["Plays"],
        request=PlayWriteSerializer,
        responses={200: PlaySerializer},
    ),
    partial_update=extend_schema(
        summary="Partially update play",
        tags=["Plays"],
        request=PlayWriteSerializer,
        responses={200: PlaySerializer},
    ),
    destroy=extend_schema(summary="Delete play", tags=["Plays"]),
)
class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("actors", "genres")
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return PlayWriteSerializer
        return PlaySerializer

    search_fields = ("title", "actors__first_name", "actors__last_name", "genres__name")


@extend_schema_view(
    list=extend_schema(
        summary="List halls",
        tags=["Theatre halls"],
        responses={200: TheatreHallSerializer(many=True)},
    ),
    retrieve=extend_schema(summary="Retrieve hall", tags=["Theatre halls"]),
    create=extend_schema(summary="Create hall", tags=["Theatre halls"]),
    update=extend_schema(summary="Update hall", tags=["Theatre halls"]),
    partial_update=extend_schema(
        summary="Partially update hall", tags=["Theatre halls"]
    ),
    destroy=extend_schema(summary="Delete hall", tags=["Theatre halls"]),
)
class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("name",)


@extend_schema_view(
    list=extend_schema(
        summary="List performances",
        tags=["Performances"],
        parameters=[
            OpenApiParameter(
                name="date",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description="Filter by calendar date (YYYY-MM-DD).",
            ),
        ],
        responses={200: PerformanceSerializer(many=True)},
    ),
    retrieve=extend_schema(summary="Retrieve performance", tags=["Performances"]),
    create=extend_schema(summary="Create performance", tags=["Performances"]),
    update=extend_schema(summary="Update performance", tags=["Performances"]),
    partial_update=extend_schema(
        summary="Partially update performance", tags=["Performances"]
    ),
    destroy=extend_schema(summary="Delete performance", tags=["Performances"]),
)
class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("play", "theatre_hall")
    serializer_class = PerformanceSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = PerformanceFilter
    ordering = ("show_time",)


@extend_schema_view(
    list=extend_schema(
        summary="List my reservations",
        tags=["Reservations"],
        responses={200: ReservationSerializer(many=True)},
    ),
    retrieve=extend_schema(summary="Retrieve my reservation", tags=["Reservations"]),
    create=extend_schema(
        summary="Create reservation",
        tags=["Reservations"],
        request=ReservationCreateSerializer,
        responses={201: ReservationSerializer},
        examples=[
            OpenApiExample(
                "Simple payload",
                value={
                    "tickets": [
                        {"row": 1, "seat": 5, "performance": 1},
                        {"row": 1, "seat": 6, "performance": 1},
                    ]
                },
            )
        ],
    ),
    destroy=extend_schema(
        summary="Cancel my reservation", tags=["Reservations"], responses={204: None}
    ),
)
class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (
            Reservation.objects.filter(user=self.request.user)
            .prefetch_related(
                "tickets__performance__play", "tickets__performance__theatre_hall"
            )
            .order_by("-id")
        )

    def get_serializer_class(self):
        if self.action == "create":
            return ReservationCreateSerializer
        return ReservationSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List my tickets",
        tags=["Tickets"],
        responses={200: TicketSerializer(many=True)},
    ),
    retrieve=extend_schema(summary="Retrieve my ticket", tags=["Tickets"]),
)
class TicketViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Ticket.objects.filter(
            reservation__user=self.request.user
        ).select_related(
            "performance__play", "performance__theatre_hall", "reservation"
        )

    serializer_class = TicketSerializer


@extend_schema_view(
    retrieve=extend_schema(
        summary="Get current user profile", tags=["Me"], responses=UserSerializer
    ),
)
class MeViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
