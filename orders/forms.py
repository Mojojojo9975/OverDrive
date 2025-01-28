from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
        'first_name',
        'last_name',
        'email',
        'phone_numer',
        'address',
        'postal_code',
        'city'
        ]