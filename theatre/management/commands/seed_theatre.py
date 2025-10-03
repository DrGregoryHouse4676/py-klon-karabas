from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from theatre.models import Actor, Genre, Play, TheatreHall, Performance
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class Command(BaseCommand):
    help = "Seed initial theatre data"

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin")
            self.stdout.write(self.style.SUCCESS("Created superuser admin/admin"))

        actors = [("Will", "Smith"), ("Johni", "Depp"), ("Lev", "Ivanov")]
        actor_objs = [
            Actor.objects.get_or_create(first_name=f, last_name=l)[0] for f, l in actors
        ]
        genres = ["Dram", "Comedy", "Musicl"]
        genre_objs = [Genre.objects.get_or_create(name=n)[0] for n in genres]
        play, _ = Play.objects.get_or_create(title="Bad Boys 5", description="Action")
        play.actors.set(actor_objs[:2])
        play.genres.set(genre_objs[:2])

        hall, _ = TheatreHall.objects.get_or_create(
            name="Велика сцена", rows=10, seats_in_row=12
        )
        base = make_aware(datetime.now() + timedelta(days=1))
        for i in range(3):
            Performance.objects.get_or_create(
                play=play,
                theatre_hall=hall,
                show_time=base + timedelta(days=i, hours=i),
            )
        self.stdout.write(self.style.SUCCESS("Seeded theatre data"))
