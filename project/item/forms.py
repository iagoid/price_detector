from django import forms

from .models import Item

class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['link'].label = ""

    class Meta:
        model = Item
        fields = ('link', )