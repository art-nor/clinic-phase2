from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser, Group, Permission, User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email', 'password1', 'password2']
class RoleForm(forms.ModelForm):
    role = forms.ChoiceField(choices=CustomUser.ROLES, required=True)
    class Meta:
        model = CustomUser
        fields = ['role']

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


from .models import Queueing
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Queueing
        fields = ['clinic', 'datetime']  # Add other fields as needed
        widgets = {
            'datetime': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)


class CancelReservationForm(forms.Form):
    reservation_id = forms.ModelChoiceField(queryset=Queueing.objects.filter(status='confirmed'), empty_label=None, label='Select Reservation to Cancel')


class IncreaseAvailabilityForm(forms.Form):
    additional_availability = forms.IntegerField(min_value=1, label='Enter Additional Availability')
