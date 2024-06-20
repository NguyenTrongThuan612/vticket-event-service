from datetime import date, datetime, timedelta
import json
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
        
        if end_date > event.start_date:
            end_date = event.start_date - timedelta(days=1)
        
        if end_date - start_date > timedelta(days=9):
            start_date = end_date - timedelta(days=9)

        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        event_id = event.id
        event_name = event.name

        statistic_data = []
        total_ticket_sold = 0
        total_revenue = 0
        for single_date in date_range:
                
            ticket_sold = UserTicket.objects.filter(
                    seat__ticket_type__event_id=event_id,
                    paid_at__date=single_date,
                    is_refunded=False
                ).count()
            total_ticket_sold += ticket_sold
            revenue = 0

            if ticket_sold != 0:
                user_tickets = UserTicket.objects.filter(
                    seat__ticket_type__event_id=event_id,
                    paid_at__date=single_date,
                    is_refunded=False,
                    payment_id__isnull=False
                )
  
                payment_ids = user_tickets.values_list('payment_id', flat=True)
                    
                response = requests.post(
                    url=f'{RelatedService.payment}/payment/list',
                    headers={
                        "Content-type": "application/json"
                    },
                    data=json.dumps(
                        {
                            "payment_ids": list(payment_ids)
                        }
                    )
                )

                resp_data = response.json()
                total_amount = resp_data['data'].get('total_amount')
                if total_amount is not None:
                    revenue += total_amount
                    total_revenue += total_amount  
                
            statistic_data.append({
                'date': single_date,
                'ticket_sold': ticket_sold,
                'revenue': revenue
            })
            
        result = {
            'id': event_id,
            'name': event_name,
            'statistic': statistic_data,
            'total_ticket_sold': total_ticket_sold,
            'total_revenue': total_revenue
        }
        return result  
    
    def total_ticket_sold_and_revenue(self, start_date: str, end_date: str) -> dict:
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


        if end_date - start_date > timedelta(days=9):
            start_date = end_date - timedelta(days=9)

            
        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        statistic_by_day = []
        total_ticket_sold = 0
        total_revenue = 0
        for single_date in date_range:
                
            ticket_sold = UserTicket.objects.filter(
                    paid_at__date=single_date,
                    is_refunded=False
                ).count()
            
            total_ticket_sold += ticket_sold
            revenue = 0

            if ticket_sold != 0:
                user_tickets = UserTicket.objects.filter(
                    paid_at__date=single_date,
                    is_refunded=False,
                    payment_id__isnull=False
                )

                payment_ids = user_tickets.values_list('payment_id', flat=True)
                    
                response = requests.post(
                    url=f'{RelatedService.payment}/payment/list',
                    headers={
                        "Content-type": "application/json"
                    },
                    data=json.dumps(
                        {
                            "payment_ids": list(payment_ids)
                        }
                    )
                )

                resp_data = response.json()
                total_amount = resp_data['data'].get('total_amount')
                if total_amount is not None:
                    revenue += total_amount
                    total_revenue += total_amount  

            statistic_by_day.append({
                'date': single_date,
                'ticket_sold': ticket_sold,
                'revenue': revenue
            })

        result = {
            'statistic_by_day': statistic_by_day,
            'total_ticket_sold': total_ticket_sold,
            'total_revenue': total_revenue
        }
        return result 

