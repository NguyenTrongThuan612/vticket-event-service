from dataclasses import asdict
from datetime import datetime
from typing import Union

from vticket_app.enums.instance_error_enum import InstanceErrorEnum
from vticket_app.models.promotion import Promotion
from vticket_app.dtos.create_promotion_dto import CreatePromotionDto
from vticket_app.serializers.promotion_serializer import PromotionSerializer
from vticket_app.dtos.user_dto import UserDTO

class PromotionService():
    def create_promotion(self, data: CreatePromotionDto) -> bool:
        try:
            _data = asdict(data)

            instance = Promotion(**_data)
            instance.save()

            if instance.id is None:
                return False
            
            return True
        except Exception as e:
            print(e)
            return False
        
    def get_promotions_by_event_id(self, event_id: int) -> list[dict]:
        queryset = Promotion.objects.filter(event__id=event_id, deleted_at=None)
        return PromotionSerializer(queryset, many=True).data
    
    def get_promotion_by_id(self, id: int) -> Union[Promotion|None]:
        try:
            return Promotion.objects.get(id=id)
        except:
            return None
    
    def delete_promotion(self, promotion: Promotion) -> InstanceErrorEnum:
        try:
            if promotion.deleted_at is not None:
                return InstanceErrorEnum.DELETED
            
            promotion.deleted_at = datetime.now()
            promotion.save(update_fields=["deleted_at"])

            return InstanceErrorEnum.ALL_OK
        except Exception as e:
            print(e)
            raise(e)
        
    def update_promotion(self, promotion: Promotion, update_data: dict) -> bool:
        try:
            for k, v in update_data.items():
                setattr(promotion, k, v)

            promotion.save(update_fields=update_data.keys())
                  
            return True
        except Exception as e:
            print(e)
            return False
        
    def modifiable(self, promotion: Promotion, user: UserDTO) -> bool:
        return promotion.event.owner_id == user.id