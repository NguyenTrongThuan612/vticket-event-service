from dataclasses import dataclass
from datetime import date, datetime

from vticket_app.enums.discount_type_enum import DiscountTypeEnum
from vticket_app.dtos.promotion_condition_dto import PromotionConditionDto

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
    promotion_condition: PromotionConditionDto = None

    def __post_init__(self):
        self.discount_type = (DiscountTypeEnum)(self.discount_type)
        self.promotion_condition = PromotionConditionDto(**self.promotion_condition)