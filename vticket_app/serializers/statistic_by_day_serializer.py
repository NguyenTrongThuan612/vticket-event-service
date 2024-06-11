from rest_framework import serializers

class StatisticByDaySerializer(serializers.Serializer):
    date = serializers.DateField()
    ticket_sold = serializers.IntegerField()
    revenue = serializers.IntegerField()