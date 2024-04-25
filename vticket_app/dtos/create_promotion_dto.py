from dataclasses import dataclass
from datetime import date, datetime

from vticket_app.enums.discount_type_enum import DiscountTypeEnum
from vticket_app.enums.promotion_evaluation_field_enum import PromotionEvaluationFieldEnum
from vticket_app.enums.promotion_evaluation_condition_enum import PromotionEvaluationConditionEnum

@dataclass
class CreatePromotionDto():
    id: int = None
    event: int = None
    discount_type: DiscountTypeEnum = None
    discount_value: int = None
    maximum_reduction_amount: int = None
    quantity: int = None
    start_date: date = None
    end_date: date = None
    deleted_at: datetime = None
    evaluation_field: PromotionEvaluationFieldEnum = None
    condition: PromotionEvaluationConditionEnum = None
    evaluation_value: int = None

    def __post_init__(self):
        self.discount_type = (DiscountTypeEnum)(self.discount_type)
        self.evaluation_field = (PromotionEvaluationFieldEnum)(self.evaluation_field)
        self.condition = (PromotionEvaluationConditionEnum)(self.condition)