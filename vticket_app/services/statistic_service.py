from datetime import date, datetime, timedelta
from django.forms import ValidationError
import requests
import time
from vticket_app.configs.related_services import RelatedService
from vticket_app.models.event import Event
from vticket_app.models.user_ticket import UserTicket
from django.db.models import Q, Case, When, Value, BooleanField, Sum, Count

class StatisticService:
    
    def ticket_sold_and_revenue_by_event(self, event: Event, start_date: str, end_date: str) -> dict:

        if start_date is not None:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("start_date phải có định dạng YYYY-MM-DD")
        if end_date is not None:
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("end_date phải có định dạng YYYY-MM-DD")
        
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        today = date.today()
        if end_date > today:
            end_date = today

        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        event_id = event.id
        event_name = event.name

        statistic_data = []

        for single_date in date_range:
                
            tickets_sold = UserTicket.objects.filter(
                    seat__ticket_type__event_id=event_id,
                    paid_at__date=single_date,
                    is_refunded=False
                ).count()
            
            total_revenue = 0

            if tickets_sold != 0:
                user_tickets = UserTicket.objects.filter(
                    seat__ticket_type__event_id=event_id,
                    paid_at__date=single_date,
                    is_refunded=False,
                    payment_id__isnull=False
                )

                payment_ids = user_tickets.values_list('payment_id', flat=True)
                    
                for payment_id in payment_ids:
                    response = requests.get(
                        url=f'{RelatedService.payment}/payment/{payment_id}',
                        headers={
                            "Content-type": "application/json"
                        }
                    )
                        
                    if response.status_code == 200:
                        payment_data = response.json()
                        if payment_data['status'] == 1 and payment_data['data'] is not None:
                            amount = payment_data['data'].get('amount')
                            if amount is not None:
                                total_revenue += amount    
                                
                
            statistic_data.append({
                'date': single_date,
                'ticket_sold': tickets_sold,
                'revenue': total_revenue
            })
            
        result = {
            'id': event_id,
            'name': event_name,
            'statistic': statistic_data
        }
        return result  
    
    def total_ticket_sold_and_revenue(self, start_date: str, end_date: str) -> list:
        if start_date is not None:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("start_date phải có định dạng YYYY-MM-DD")
        if end_date is not None:
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("end_date phải có định dạng YYYY-MM-DD")
        
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        today = date.today()
        if end_date > today:
            end_date = today

        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        statistic_data = []

        for single_date in date_range:
                
            tickets_sold = UserTicket.objects.filter(
                    paid_at__date=single_date,
                    is_refunded=False
                ).count()
            
            total_revenue = 0

            if tickets_sold != 0:
                user_tickets = UserTicket.objects.filter(
                    paid_at__date=single_date,
                    is_refunded=False,
                    payment_id__isnull=False
                )

                payment_ids = user_tickets.values_list('payment_id', flat=True)
                    
                for payment_id in payment_ids:
                    response = requests.get(
                        url=f'{RelatedService.payment}/payment/{payment_id}',
                        headers={
                            "Content-type": "application/json"
                        }
                    )
                        
                    if response.status_code == 200:
                        payment_data = response.json()
                        if payment_data['status'] == 1 and payment_data['data'] is not None:
                            amount = payment_data['data'].get('amount')
                            if amount is not None:
                                total_revenue += amount    
                                
                
            statistic_data.append({
                'date': single_date,
                'ticket_sold': tickets_sold,
                'revenue': total_revenue
            })

        return statistic_data  
