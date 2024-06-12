import datetime
from rest_framework import serializers

from vticket_app.models.feedback import Feedback
from vticket_app.models.user_ticket import UserTicket

class UserTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTicket
        fields = "__all__"

    feedbackable = serializers.SerializerMethodField()
    seat_number = serializers.SerializerMethodField()
    event_name = serializers.SerializerMethodField()
    event_start_date = serializers.SerializerMethodField()
    event_id = serializers.SerializerMethodField()
    ticket_status = serializers.SerializerMethodField()
    
    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(existing - fields):
            self.fields.pop(field, None)

    def get_feedbackable(self, obj: UserTicket):
        return (
            obj.is_refunded == False 
            and obj.seat.ticket_type.event.start_date <= datetime.datetime.now().date()
            and not Feedback.objects.filter(event=obj.seat.ticket_type.event, owner_id=self.context["user_id"]).exists()
        )
    
    def get_seat_number(self, obj):
        return f"{obj.seat.position}{obj.seat.seat_number}"
    
    def get_event_name(self, obj):
        return obj.seat.ticket_type.event.name
    
    def get_event_start_date(self, obj):
        return obj.seat.ticket_type.event.start_date.strftime("%d-%m-%Y")
    
    def get_event_id(self, obj):
        return obj.seat.ticket_type.event.id
    
    def get_ticket_status(self, obj):
        if obj.payment_id:
            return "paid"
        if obj.payment_id is None:
            return "wait_to_pay"
        if obj.is_refunded:
            return "refund"