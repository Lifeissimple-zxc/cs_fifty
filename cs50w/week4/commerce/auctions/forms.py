from django import forms
from . import models


class NewListingForm(forms.ModelForm):
    "POST request form with data needed to create a new listing"
    class Meta:
        model = models.Listing
        exclude = ["id", "status", "user"]
        widgets = {
            "title": forms.TextInput(),
            "starting_bid": forms.NumberInput(),
            "description": forms.TextInput(),
            "image_url": forms.TextInput(),
            "category": forms.Select(choices=models.ListingCategory.objects.all())
        }


