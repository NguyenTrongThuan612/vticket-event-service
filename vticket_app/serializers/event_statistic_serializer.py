from rest_framework import serializers
from vticket_app.serializers.statistic_serializer import StatisticSerializer

class EventStatisticSerialize(serializers.Serializer):
    id = serializers.IntegerField(allow_null=False)
    name = serializers.CharField()
    statistic = StatisticSerializer(many=True)
    total_ticket_sold = serializers.IntegerField()
    total_revenue = serializers.IntegerField()