from rest_framework import serializers
from vticket_app.models.feedback import Feedback
from vticket_app.serializers.feedback_serializer import FeedbackSerializer

class CreateFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        exclude = ["owner_id"]