from django.shortcuts import render, redirect
from .forms import ReservationForm
from .models import Reservation
from .google_calendar import create_google_calendar_event
from django.http import HttpResponse
from googleapiclient.errors import HttpError

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
    return render(request, 'thank_you.html')

def oauth2callback(request):
    return HttpResponse("OAuth2 callback received.")