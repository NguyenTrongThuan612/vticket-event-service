from rest_framework import serializers

class CreateSeatConfigurationValidator(serializers.Serializer):
    position = serializers.CharField()
    start_seat_number = serializers.IntegerField(min_value=1)
    end_seat_number = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        _validated_data = super().validate(attrs)

        if _validated_data["start_seat_number"] > _validated_data["end_seat_number"]:
            raise serializers.ValidationError("Start seat number must be equal to or less than end seat number!")

        return super().validate(attrs)