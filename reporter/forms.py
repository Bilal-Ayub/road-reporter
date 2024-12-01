from django import forms
from .models import Report
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_type', 'report_description', 'location_lat', 'location_lon', 'image', 'priority']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = f"{self.cleaned_data['first_name'].lower()}{self.cleaned_data['last_name'].lower()}@gmail.com"

        # Generate a username
        username = f"{self.cleaned_data['first_name'].lower()}{self.cleaned_data['last_name'].lower()}"

        # Ensure the username is unique
        if User.objects.filter(username=username).exists():
            username += str(User.objects.filter(username__startswith=username).count() + 1)

        user.username = username

        if commit:
            user.save()
        return user