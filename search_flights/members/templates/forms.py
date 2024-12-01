from django import forms

class FlightSearchForm(forms.Form):
    origin = forms.CharField(max_length=3, label="Origin Airport Code")
    destination = forms.CharField(max_length=3, label="Destination Airport Code")
    start_date = forms.DateField(label="Departure Date", widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label="Return Date", widget=forms.DateInput(attrs={'type': 'date'}))