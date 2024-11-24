from django import forms
from .models import Reservation
import datetime
from django.db.models import Sum

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer_name', 'email', 'date', 'time', 'num_of_people']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        # Ensure the reservation date is Saturday or Sunday
        if date.weekday() not in [5, 6]:
            raise forms.ValidationError("Reservations are only allowed for Saturdays and Sundays.")
        return date
    
    def clean_time(self):
        time = self.cleaned_data.get('time')
        # Ensure the reservation time is between 8:00am and 4:00pm
        if not (datetime.time(8, 0) <= time <= datetime.time(16, 0)):
            raise forms.ValidationError("Reservations are only allowed between 8:00am and 4:00pm.")
        return time
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        num_of_people = cleaned_data.get('num_of_people')

        if date and time and num_of_people:
            # Check the total number of people already reserved for this date and time
            existing_reservations = Reservation.objects.filter(date=date, time=time)
            total_people = existing_reservations.aggregate(Sum('num_of_people'))['num_of_people__sum'] or 0

            if total_people + num_of_people > 15:
                raise forms.ValidationError(f"Capacity exceeded for this date and time. Only {15 - total_people} seats are available.")
        return cleaned_data