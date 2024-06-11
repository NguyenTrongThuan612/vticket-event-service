from rest_framework import serializers

from vticket_app.serializers.statistic_by_day_serializer import StatisticByDaySerializer

class StatisticSerializer(serializers.Serializer):
    statistic_by_day = StatisticByDaySerializer(many=True)
    total_ticket_sold = serializers.IntegerField()
    total_revenue = serializers.IntegerField()