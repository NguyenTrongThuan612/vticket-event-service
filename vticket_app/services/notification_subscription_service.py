from django.core.exceptions import ObjectDoesNotExist

from vticket_app.models.notification_subscription import NotificationSubscription

class NotificationSubcriptionService():
    def get_subscription_status_by_email(self, email: str) -> bool:
        try:
            ns = NotificationSubscription.objects.get(email=email)

            return ns.deleted_at == None
        except ObjectDoesNotExist:
            self.__auto_create_subscription(email=email)
            return True
        except Exception as e:
            print(e)
            return False
        
    def change_subscription_status_by_email(self, email: str) -> bool:
        try:
            ns = NotificationSubscription.objects.get(email=email)
            ns.change_status()
            return True
        except Exception as e:
            print(e)
            return False
        
    def __auto_create_subscription(self, email: str):
        try:
            ns = NotificationSubscription(email=email)
            ns.save()
        except Exception as e:
            print(e)