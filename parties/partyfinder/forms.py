from django import forms

class PartyForm(forms.Form):
    city = forms.CharField(label='City', max_length=50)
    name = forms.CharField(label='Name', max_length=200)
    date = forms.DateField(label='Date (YYYY-MM-DD)', input_formats=['%Y-%m-%d'])
    people = forms.IntegerField(label='People', min_value=0)

class CityForm(forms.Form):
    city = forms.CharField(label='Browse city:', max_length=50)
