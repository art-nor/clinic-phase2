from django.urls import path
from .views import clinic_selection
from .views import clinic_options, view_current_appointments, cancel_reservations, increase_availability
from . import views

urlpatterns = [
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view , name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('current_appointments', views.current_appointments, name='current_appointments'),
    path('appointment_history', views.appointment_history, name='appointment_history'),
    path('new_reservation', views.new_reservation, name='new_reservation'),
    path('clinic_selection/', views.clinic_selection, name='clinic_selection'),
    path('clinic_options/<int:clinic_id>/', views.clinic_options, name='clinic_options'),
    path('view_current_appointments/<int:clinic_id>/', views.view_current_appointments, name='view_current_appointments'),
    path('cancel_reservations/<int:clinic_id>/', views.cancel_reservations, name='cancel_reservations'),
    path('increase_availability/<int:clinic_id>/', views.increase_availability, name='increase_availability'),
]

