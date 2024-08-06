import logging
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from store.models import Customer, Address
from django.contrib.auth.models import User


class CustomerProfileEditForm(forms.ModelForm):

    first_name = forms.CharField(min_length=2, max_length=100)
    last_name = forms.CharField(min_length=2, max_length=100)
    email = forms.EmailField(min_length=8, max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Save', css_class="btn btn-secondary"))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).exclude(pk=self.instance.user.pk)
        if user:
            self.add_error('email', 'Email already been used, please use different email.')
        return email

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit is True:
            user = instance.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
        instance.save()
        return instance

    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'email',
            'company', 'phone_number', 'date_of_birth', 'gender'
        ]


class CustomerAddressEditForm(forms.ModelForm):

    def __init__(self, customer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = customer
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Save', css_class="btn btn-secondary"))

    def save(self, commit=True):
        self.instance.customer = self.customer
        return super().save(commit=commit)

    class Meta:
        model = Address
        fields = [
            'contact_phone_number', 'contact_email',
            'unit', 'street', 'city', 'state', 'postcode',
            'country', 'is_billing', 'note', 'is_default'
        ]


class CustomerAddressCreateForm(forms.ModelForm):

    def __init__(self, customer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = customer
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', 'Save', css_class="btn btn-secondary"))

    def save(self, commit=True):
        self.instance.customer = self.customer
        return super().save(commit=commit)

    class Meta:
        model = Address
        fields = [
            'contact_phone_number', 'contact_email',
            'unit', 'street', 'city', 'state', 'postcode',
            'country', 'is_billing', 'note', 'is_default'
        ]