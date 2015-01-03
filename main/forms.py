from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Link


class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))

    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form


class MikiForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'class': 'MikiTitle', 'placeholder': 'Title (max = 50 chars)'}))
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'class': 'MikiBody', 'placeholder': 'Body (max = 200 chars)', 'rows': '3'}))

    def is_valid(self):
        form = super(MikiForm, self).is_valid()
        for f in self.errors.iterkeys():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error MikiText'})
        return form

    class Meta:
        model = Link
        exclude = ('user',)
