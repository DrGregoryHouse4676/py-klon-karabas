from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Actor(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    class Meta:
        ordering = ("last_name", "first_name")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Play(models.Model):
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    actors = models.ManyToManyField(Actor, related_name="plays", blank=True)
    genres = models.ManyToManyField(Genre, related_name="plays", blank=True)

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=64, unique=True)
    rows = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    seats_in_row = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name} ({self.rows}x{self.seats_in_row})"

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row


class Performance(models.Model):
    play = models.ForeignKey(
        Play, on_delete=models.PROTECT, related_name="performances"
    )
    theatre_hall = models.ForeignKey(
        TheatreHall, on_delete=models.PROTECT, related_name="performances"
    )
    show_time = models.DateTimeField()

    class Meta:
        ordering = ("show_time",)
        indexes = [models.Index(fields=["show_time"])]
        constraints = [
            models.UniqueConstraint(
                fields=["theatre_hall", "show_time"], name="unique_hall_timeslot"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.play.title} @ {self.theatre_hall.name} {self.show_time:%Y-%m-%d %H:%M}"


class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Reservation #{self.pk} by {self.user}"


class Ticket(models.Model):
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    class Meta:
        ordering = ("performance", "row", "seat")
        constraints = [
            models.UniqueConstraint(
                fields=["performance", "row", "seat"],
                name="unique_seat_per_performance",
            ),
            models.CheckConstraint(
                check=models.Q(row__gt=0) & models.Q(seat__gt=0),
                name="row_seat_positive",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.performance} — r{self.row}s{self.seat}"
