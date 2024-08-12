from django import forms

FUEL_CHOICES = [
    ('Petrol', 'Petrol'),
    ('Diesel', 'Diesel'),
    # Add more fuel types if needed
]

class CarPriceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        car_choices = kwargs.pop('car_choices', [])
        super(CarPriceForm, self).__init__(*args, **kwargs)
        self.fields['car_name'] = forms.ChoiceField(choices=car_choices, label='Car Name')
        self.fields['present_price'] = forms.FloatField(label='Present Price (in lakhs)')
        self.fields['kms_driven'] = forms.IntegerField(label='Kms Driven')
        self.fields['fuel_type'] = forms.ChoiceField(choices=FUEL_CHOICES, label='Fuel Type')
        self.fields['seller_type'] = forms.ChoiceField(choices=[('Dealer', 'Dealer'), ('Individual', 'Individual')], label='Seller Type')
        self.fields['transmission'] = forms.ChoiceField(choices=[('Manual', 'Manual'), ('Automatic', 'Automatic')], label='Transmission')
        self.fields['owner'] = forms.ChoiceField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3')], label='Owner')
        self.fields['year'] = forms.IntegerField(label='Year of Purchase')
