from rest_framework import serializers

from vticket_app.enums.discount_type_enum import DiscountTypeEnum
from vticket_app.enums.promotion_evaluation_field_enum import PromotionEvaluationFieldEnum
from vticket_app.enums.promotion_evaluation_condition_enum import PromotionEvaluationConditionEnum

class UpdatePromotionSerializer(serializers.Serializer):
    discount_type = serializers.ChoiceField(required=False, choices=DiscountTypeEnum.values)
    discount_value = serializers.IntegerField(required=False, min_value=1)
    maximum_reduction_amount = serializers.IntegerField(required=False, min_value=1)
    quantity = serializers.IntegerField(required=False, min_value=1)
    evaluation_field = serializers.ChoiceField(required=False, choices=PromotionEvaluationFieldEnum.values)
    condition = serializers.ChoiceField(required=False, choices=PromotionEvaluationConditionEnum.values)
    evaluation_value = serializers.IntegerField(required=False, min_value=1)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)