import pandas as pd
from itertools import chain
from rest_framework import serializers

from vticket_app.serializers.event_serializer import EventSerializer
from vticket_app.serializers.create_ticket_type_serializer import CreateTicketTypeSerializer

class CreateEventSerializer(EventSerializer):
    ticket_types = CreateTicketTypeSerializer(many=True, allow_empty=False, min_length=1, exclude=["event"])
    
    def validate(self, attrs):
        _validated_data = super().validate(attrs)
        _seats = list(chain.from_iterable([data["seat_configurations"] for data in _validated_data["ticket_types"]]))
        _grouped_seats = pd.DataFrame(_seats).groupby("position")

        for _, group in _grouped_seats:
            _seat_pairs = [(row['start_seat_number'], row['end_seat_number']) for _, row in group.iterrows()]

            if self.__check_intersection(_seat_pairs):
                raise serializers.ValidationError("Overlapping seat configurations occur!")

        return _validated_data
    
    def __check_intersection(self, pairs: list[tuple[int, int]]) -> bool:
        sorted_pairs = sorted(pairs, key=lambda x: x[0])

        for i in range(len(sorted_pairs) - 1):
            if sorted_pairs[i][1] >= sorted_pairs[i + 1][0]:
                return True
        return False