from rest_framework import serializers

from vticket_app.enums.discount_type_enum import DiscountTypeEnum
from vticket_app.enums.promotion_evaluation_condition_enum import PromotionEvaluationConditionEnum
from vticket_app.models.promotion import Promotion

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"

    pretty_name = serializers.SerializerMethodField()
        
    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(existing - fields):
            self.fields.pop(field, None)

    def validate(self, attrs):
        _validated_data = super().validate(attrs)

        if _validated_data["start_date"] > _validated_data["end_date"]:
            raise serializers.ValidationError("Start date must be equal to or less than end date!")
        
        return _validated_data
    
    def __condition_to_semantic(self, condition: PromotionEvaluationConditionEnum):
        return {
            PromotionEvaluationConditionEnum.gt: "lớn hơn",
            PromotionEvaluationConditionEnum.gte: "từ",
            PromotionEvaluationConditionEnum.lt: "nhỏ hơn",
            PromotionEvaluationConditionEnum.lte: "tối đa",
        }[condition]
    
    def get_pretty_name(self, obj: Promotion):
        long_content = ""
        short_content = ""
        condition_semantic = self.__condition_to_semantic(obj.condition)

        if obj.discount_type == DiscountTypeEnum.cash:
            long_content = f"Giảm {obj.discount_value} VNĐ cho hóa đơn có giá trị {condition_semantic} {obj.evaluation_value} VNĐ"
            short_content = f"Giảm {obj.discount_value} VNĐ"
        elif obj.discount_type == DiscountTypeEnum.percent:
            long_content = f"Giảm {obj.discount_value}% (tối đa {obj.maximum_reduction_amount} VNĐ) cho hóa đơn có giá trị {condition_semantic} {obj.evaluation_value}"
            short_content = f"Giảm {obj.discount_value}%"

        return {
            "short_content": short_content, 
            "long_content": long_content
        }
