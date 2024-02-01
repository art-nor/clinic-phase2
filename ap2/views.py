from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import *

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        roles = RoleForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = roles.save()
            user.role = role
            # Create 'Staff' and 'Patient' groups if they don't exist
            staff_group, created_staff = Group.objects.get_or_create(name='Staff')
            patient_group, created_patient = Group.objects.get_or_create(name='Patient')

            # Add user to the appropriate group based on their role
            if user.role == 'staff' and created_staff:
                staff_group.user_set.add(user)
            elif user.role == 'patient' and created_patient:
                patient_group.user_set.add(user)

            return redirect('login')  # Redirect to your home page
    else:
        form = SignupForm()
        roles = RoleForm

    return render(request, 'signup.html', {'form': form,'roles':roles})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to your home page
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# your_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Queueing
from .forms import ReservationForm  # You need to define a ReservationForm

#@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

#@login_required
def current_appointments(request):
    user = request.user
    appointments = Queueing.objects.filter(user=user, status='confirmed')  # Adjust the filter condition as needed
    return render(request, 'current_appointments.html', {'appointments': appointments})

#@login_required
def appointment_history(request):
    user = request.user
    appointments_history = Queueing.objects.filter(user=user)  # You might want to filter completed or canceled appointments
    return render(request, 'appointment_history.html', {'appointments_history': appointments_history})


# your_app/views.py
from .forms import ReservationForm

#@login_required
def new_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.status = 'pending'  # You can set the initial status as needed
            reservation.appointment_cost = 0  # You can set the initial cost as needed
            reservation.save()
            return redirect('current_appointments')  # Redirect to current appointments after successful reservation
    else:
        form = ReservationForm()

    return render(request, 'newreservation.html', {'form': form})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Clinic

@login_required
def clinic_selection(request):
    # Retrieve all clinics for the employee to choose from
    clinics = Clinic.objects.all()
   
    return render(request, 'your_app/clinic_selection.html', {'clinics': clinics})

from django.shortcuts import render, redirect
from .models import Clinic, Queueing

@login_required
def clinic_options(request, clinic_id):
    clinic = Clinic.objects.get(pk=clinic_id)

    return render(request, 'your_app/clinic_options.html', {'clinic': clinic})

from django.shortcuts import render
from .models import Clinic, Queueing

@login_required
def view_current_appointments(request, clinic_id):
    clinic = Clinic.objects.get(pk=clinic_id)
    appointments = Queueing.objects.filter(clinic=clinic, status='confirmed')
   
    return render(request, 'your_app/view_current_appointments.html', {'clinic': clinic, 'appointments': appointments})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CancelReservationForm, IncreaseAvailabilityForm

@login_required
def cancel_reservations(request, clinic_id):
    clinic = Clinic.objects.get(pk=clinic_id)

    if request.method == 'POST':
        form = CancelReservationForm(request.POST)
        if form.is_valid():
            reservation_id = form.cleaned_data['reservation_id']

            try:
                reservation = Queueing.objects.get(pk=reservation_id, status='confirmed', clinic=clinic)
                # Optionally, you may want to add further checks before canceling, e.g., datetime validation

                reservation.status = 'canceled'
                reservation.save()

                messages.success(request, 'Reservation canceled successfully.')
            except Queueing.DoesNotExist:
                messages.error(request, 'Invalid reservation ID or reservation cannot be canceled.')

            return redirect('clinic_options', clinic_id=clinic_id)
    else:
        form = CancelReservationForm()

    return render(request, 'your_app/cancel_reservations.html', {'clinic': clinic, 'form': form})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CancelReservationForm, IncreaseAvailabilityForm

@login_required
def increase_availability(request, clinic_id):
    clinic = Clinic.objects.get(pk=clinic_id)

    if request.method == 'POST':
        form = IncreaseAvailabilityForm(request.POST)
        if form.is_valid():
            additional_availability = form.cleaned_data['additional_availability']

            try:
                # Retrieve the clinic and update its availability
                clinic = Clinic.objects.get(pk=clinic_id)
                clinic.availability += additional_availability
                clinic.save()

                messages.success(request, 'Availability increased successfully.')
            except Clinic.DoesNotExist:
                messages.error(request, 'Invalid clinic ID.')

            return redirect('clinic_options', clinic_id=clinic_id)
    else:
        form = IncreaseAvailabilityForm()

    return render(request, 'your_app/increase_availability.html', {'clinic': clinic, 'form': form})