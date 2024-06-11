from rest_framework import serializers

class StatisticSerializer(serializers.Serializer):
    date = serializers.DateField()
    ticket_sold = serializers.IntegerField()
    revenue = serializers.IntegerField()