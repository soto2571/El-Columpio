from django.shortcuts import render, redirect
from .forms import ReservationForm
from .models import Reservation
from .google_calendar import create_google_calendar_event
from django.http import HttpResponse
from googleapiclient.errors import HttpError
from datetime import datetime

def home(request):
    return render(request, 'index.html')

def reserve_seat(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            try:
                create_google_calendar_event(reservation)
            except HttpError as error:
                print(f"An error occurrd: {error}")
                return render(request, 'reserve.html', {
                    'form': form,
                    'error_message': "There was an error creating the calendar event. Please try again."
                })
            
            # Store data in the session
            request.session['customer_name'] = reservation.customer_name
            request.session['date'] = reservation.date.strftime('%Y-%m-%d')
            return redirect('thank_you')
        else:
            # Form is invalid
            return render(request, 'reserve.html', {
                'form': form,
                'error_message': "Please correct the errors below."
            })
    else:
        form = ReservationForm()
    return render(request, 'reserve.html', {'form': form})

def thank_you(request):
    # Retrieve data from the session
    customer_name = request.session.get('customer_name', 'Customer')
    date_str = request.session.get('date', 'a future date')

    date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str != 'a future date' else 'a future date'

    # Clear the session
    request.session.pop('customer_name', None)
    request.session.pop('date', None)

    return render(request, 'thank_you.html', {
        'customer_name': customer_name,
        'date': date,
    })

def oauth2callback(request):
    return HttpResponse("OAuth2 callback received.")