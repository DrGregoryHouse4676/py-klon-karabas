from typing import List
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from theatre.models import Reservation, Ticket, Performance


class BookingError(ValidationError):
    pass


    def _validate_seats(performance: Performance, seats: List[dict]) -> None:
        hall = performance.theatre_hall
        seen = set()
        for item in seats:
            r, s = int(item["row"]), int(item["seat"])
            if not (1 <= r <= hall.rows and 1 <= s <= hall.seats_in_row):
                raise BookingError(f"Places outside the hall range: row={r}, seat={s}")
            if (r, s) in seen:
                raise BookingError(f"Repeating a place in a query: row={r}, seat={s}")
            seen.add((r, s))


    def create_reservation(*, user, performance: Performance, seats: List[dict]) -> Reservation:
        if not seats:
            raise BookingError("The list of places is empty.")
        _validate_seats(performance, seats)

        with transaction.atomic():
            reservation = Reservation.objects.create(user=user)
            try:
                for item in seats:
                    Ticket.objects.create(
                        performance=performance,
                        reservation=reservation,
                        row=item["row"],
                        seat=item["seat"],
                    )
            except IntegrityError:
                raise BookingError("Some seats are already taken. Please refresh the layout and try again.")
        return reservation
