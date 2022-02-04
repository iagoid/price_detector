from django import forms

from .models import Item

class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['link'].label = ""

    link = forms.URLField(max_length=200, widget=forms.URLInput({ "placeholder": "Cole aqui a URL do seu produto"}))
    class Meta:
        model = Item
        fields = ('link', )