from rest_framework import serializers
from vticket_app.models.feedback import Feedback
from vticket_app.serializers.feedback_reply_serializer import FeedbackReplySerializer
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

    feedback_replies = FeedbackReplySerializer(many=True, allow_empty=False, min_length=1, exclude=["feedback"])
    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(existing - fields):
            self.fields.pop(field, None)