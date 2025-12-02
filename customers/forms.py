from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from .models import Customer

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=10)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'password1', 'password2']

    def save(self, commit=True):
        # Save User first
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            # Now create Customer
            Customer.objects.create(
                user=user,
                name=user.username,
                phone=self.cleaned_data["phone"],
                address=self.cleaned_data["address"]
            )

        return user


# Login form
class CustomLoginForm(AuthenticationForm):
    pass










        

