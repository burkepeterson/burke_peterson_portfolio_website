from django import forms
from .models import Watchlist


class WatchlistForm(forms.ModelForm):

    class Meta:
        model = Watchlist
        fields = ('user', 'ticker')
