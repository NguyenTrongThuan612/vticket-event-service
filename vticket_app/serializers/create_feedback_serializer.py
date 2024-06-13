from vticket_app.models.feedback import Feedback
from vticket_app.serializers.feedback_serializer import FeedbackSerializer

class CreateFeedbackSerializer(FeedbackSerializer):
    class Meta:
        model = Feedback
        exclude = ["owner_id"]