from django import forms


class ScrapingForm(forms.Form):
    city = forms.CharField(max_length=100)
    check_in = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    check_out = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    group_adults = forms.IntegerField(min_value=1)
    num_rooms = forms.IntegerField(min_value=1)
    group_children = forms.IntegerField(min_value=0)
    selected_currency = forms.CharField(max_length=10)
    hotel_filter = forms.BooleanField(label='Scrape Hotel Properties Only', required=False)
