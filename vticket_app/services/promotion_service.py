from dataclasses import asdict
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from vticket_app.enums.instance_error_enum import InstanceErrorEnum
from vticket_app.models.promotion import Promotion
from vticket_app.models.promotion_condition import PromotionCondition
from vticket_app.dtos.create_promotion_dto import CreatePromotionDto
from vticket_app.dtos.promotion_condition_dto import PromotionConditionDto
from vticket_app.serializers.promotion_serializer import PromotionSerializer

class PromotionService():
    def create_promotion(self, data: CreatePromotionDto) -> bool:
        try:
            _condition = data.promotion_condition
            _data = asdict(data)
            _data.pop("promotion_condition")

            instance = Promotion(**_data)
            instance.save()

            if instance.id is None:
                return False
            
            if not self._create_promotion_condition(instance, _condition):
                return False
            
            return True
        except Exception as e:
            print(e)
            return False
        
    def _create_promotion_condition(self, promotion: Promotion, data: PromotionConditionDto) -> bool:
        try:
            _parsed_data = asdict(data)
            _parsed_data.pop("id")
            _parsed_data.pop("promotion")

            instance = PromotionCondition(promotion=promotion, **_parsed_data)
            instance.save()
            
            return instance.id is not None
        except Exception as e:
            print(e)
            return False
        
    def get_promotions_by_event_id(self, event_id: int) -> list[dict]:
        queryset = Promotion.objects.filter(event__id=event_id, deleted_at=None)
        return PromotionSerializer(queryset, many=True).data
    
    def delete_promotion(self, id: int) -> InstanceErrorEnum:
        try:
            instance = Promotion.objects.get(id=id)

            if instance.deleted_at is not None:
                return InstanceErrorEnum.DELETED
            
            instance.deleted_at = datetime.now()
            instance.save(update_fields=["deleted_at"])

            return InstanceErrorEnum.ALL_OK
        except ObjectDoesNotExist:
            return InstanceErrorEnum.NOT_EXISTED
        except Exception as e:
            print(e)
            raise(e)
