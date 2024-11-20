from django import forms

class FlightSearchForm(forms.Form):
    origin = forms.CharField(label='Origin Airport Code', max_length=3)
    destination = forms.CharField(label='Destination Airport Code', max_length=3)
    start_date = forms.DateField(label='Departure Date', widget=forms.SelectDateWidget)
    end_date = forms.DateField(label='Return Date', widget=forms.SelectDateWidget)