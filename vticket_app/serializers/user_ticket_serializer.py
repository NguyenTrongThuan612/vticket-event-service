import datetime
from rest_framework import serializers

from vticket_app.models.feedback import Feedback
from vticket_app.models.user_ticket import UserTicket

class UserTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTicket
        fields = "__all__"

    feedbackable = serializers.SerializerMethodField()
    
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