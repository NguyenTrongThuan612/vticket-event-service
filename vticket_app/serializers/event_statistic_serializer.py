from rest_framework import serializers
from vticket_app.serializers.statistic_by_day_serializer import StatisticByDaySerializer

class EventStatisticSerialize(serializers.Serializer):
    id = serializers.IntegerField(allow_null=False)
    name = serializers.CharField()
    statistic = StatisticByDaySerializer(many=True)
    total_ticket_sold = serializers.IntegerField()
    total_revenue = serializers.IntegerField()