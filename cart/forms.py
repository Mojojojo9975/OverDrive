from django import forms


SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

class CartAddProductForm(forms.Form):

    size = forms.ChoiceField(
        choices=SIZE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )
    
    quantity = forms.IntegerField(
        min_value=1,
        max_value=50,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px;'}),
    )

    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )