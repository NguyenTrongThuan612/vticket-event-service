from vticket_app.models.promotion import Promotion
from vticket_app.serializers.promotion_serializer import PromotionSerializer

class CreatePromotionSerializer(PromotionSerializer):
    class Meta:
        model = Promotion
        exclude = ["deleted_at", "quantity_used"]