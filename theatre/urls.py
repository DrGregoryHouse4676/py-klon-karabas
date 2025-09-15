from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ActorViewSet, GenreViewSet, PlayViewSet, TheatreHallViewSet,
    PerformanceViewSet, ReservationViewSet, TicketViewSet, MeViewSet,
)

router = DefaultRouter()
router.register(r"actors", ActorViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"plays", PlayViewSet)
router.register(r"halls", TheatreHallViewSet)
router.register(r"performances", PerformanceViewSet)
router.register(r"reservations", ReservationViewSet, basename="reservations")
router.register(r"tickets", TicketViewSet, basename="tickets")
router.register(r"me", MeViewSet, basename="me")

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]