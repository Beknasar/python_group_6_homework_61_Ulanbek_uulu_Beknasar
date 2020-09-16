from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from accounts.models import Profile


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=commit)
        Profile.objects.create(user=user)
        return user

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        email = cleaned_data.get('email')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if not first_name:
            if not last_name:
                errors.append(ValidationError('You must fill in at least one of the specified fields: last_name, first_name'))
        if not email:
            errors.append(ValidationError('This field is required: email.'))
        if errors:
            raise ValidationError(errors)
        return cleaned_data


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']