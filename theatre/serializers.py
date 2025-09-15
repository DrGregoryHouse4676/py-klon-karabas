from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Actor, Genre, Play, TheatreHall, Performance, Reservation, Ticket
from .services.seats import build_seat_map
from .services.booking import create_reservation


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class PlaySerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ("id", "title", "description", "actors", "genres")


class PlayWriteSerializer(serializers.ModelSerializer):
    actor_ids = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all(), many=True, write_only=True, required=False)
    genre_ids = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, write_only=True, required=False)

    class Meta:
        model = Play
        fields = ("id", "title", "description", "actor_ids", "genre_ids")

    def create(self, validated_data):
        actor_ids = validated_data.pop("actor_ids", [])
        genre_ids = validated_data.pop("genre_ids", [])
        play = Play.objects.create(**validated_data)
        if actor_ids:
            play.actors.set(actor_ids)
        if genre_ids:
            play.genres.set(genre_ids)
        return play

    def update(self, instance, validated_data):
        actor_ids = validated_data.pop("actor_ids", None)
        genre_ids = validated_data.pop("genre_ids", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if actor_ids is not None:
            instance.actors.set(actor_ids)
        if genre_ids is not None:
            instance.genres.set(genre_ids)
        return instance


class TheatreHallSerializer(serializers.ModelSerializer):
    capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class PerformanceSerializer(serializers.ModelSerializer):
    play = PlaySerializer(read_only=True)
    theatre_hall = TheatreHallSerializer(read_only=True)
    play_id = serializers.PrimaryKeyRelatedField(queryset=Play.objects.all(), write_only=True, source="play")
    theatre_hall_id = serializers.PrimaryKeyRelatedField(queryset=TheatreHall.objects.all(), write_only=True,
                                                         source="theatre_hall")
    seat_map = serializers.SerializerMethodField()

    class Meta:
        model = Performance
        fields = (
            "id", "play", "theatre_hall", "show_time",
            "play_id", "theatre_hall_id", "seat_map",
        )

    def get_seat_map(self, obj):
        return build_seat_map(obj)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "performance", "row", "seat", "reservation")
        read_only_fields = ("reservation",)


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")


class ReservationCreateSerializer(serializers.Serializer):
    performance_id = serializers.PrimaryKeyRelatedField(queryset=Performance.objects.all(), source="performance")
    seats = serializers.ListField(child=serializers.DictField(child=serializers.IntegerField()), allow_empty=False)

    def create(self, validated_data):
        user = self.context["request"].user
        performance = validated_data["performance"]
        seats = validated_data["seats"]
        reservation = create_reservation(user=user, performance=performance, seats=seats)
        return reservation

    def to_representation(self, instance):
        return ReservationSerializer(instance).data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")
