from dataclasses import dataclass

from vticket_app.enums.promotion_evaluation_field_enum import PromotionEvaluationFieldEnum
from vticket_app.enums.promotion_evaluation_condition_enum import PromotionEvaluationConditionEnum

@dataclass
class PromotionConditionDto():
    id: int = None
    promotion: int = None
    evaluation_field: PromotionEvaluationFieldEnum = None
    condition: PromotionEvaluationConditionEnum = None
    value: int = None

    def __post_init__(self):
        self.evaluation_field = (PromotionEvaluationFieldEnum)(self.evaluation_field)
        self.condition = (PromotionEvaluationConditionEnum)(self.condition)