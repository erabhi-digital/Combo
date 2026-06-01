from django import forms
from django.contrib.auth import get_user_model
from .models import User



User = get_user_model()


class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class EmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email not registered")

        return email


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)