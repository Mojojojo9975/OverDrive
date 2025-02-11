from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'address',
        'postal_code',
        'city'
        ]
    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone:
            raise forms.ValidationError("Phone number is required.")
        return phone
    
    def clean_postal_code(self):
        postal_code = self.cleaned_data.get("postal_code")
        if not postal_code.isdigit():
            raise forms.ValidationError("Postal code must contain only numbers.")
        return postal_code