from typing import List, Dict, Tuple
from theatre.models import Performance


Seat = Dict[str, int]  # {"row": 1, "seat": 5}


def performance_taken_seats(performance: Performance) -> set[Tuple[int, int]]:
    # Generate a map of places and mark occupied ones
    pairs = performance.tickets.values_list("row", "seat")
    return set(pairs)


def build_seat_map(performance: Performance) -> List[List[dict]]:
    hall = performance.theatre_hall
    taken = performance_taken_seats(performance)
    grid: List[List[dict]] = []
    for r in range(1, hall.rows + 1):
        row_items = []
        for s in range(1, hall.seats_in_row + 1):
            row_items.append(
                {
                    "row": r,
                    "seat": s,
                    "is_taken": (r, s) in taken,
                }
            )
        grid.append(row_items)
    return grid
