from django import forms

class BlogForm(forms.Form):
    subject = forms.CharField()
    type = forms.CharField()
    tag = forms.CharField(required=False)
    myEditor = forms.CharField()
    content = forms.CharField()