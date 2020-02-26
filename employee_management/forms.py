from django import forms
from .models import Employee
from django.core.validators import RegexValidator


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'phone_number', 'email_address',
                  'emp_code', 'position', 'manager_name')
        labels = {'email_address': 'Email',
                  'emp_code': 'Employee Code',
                  'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'phone_number': 'Phone Number',
                  'manager_name': 'Manager Name'}
        widgets = {
            "phone_number": forms.TextInput(attrs={"placeholder": "xxx-xxx-xxxx"})
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['position'].empty_label = 'Select'
        self.fields['manager_name'].empty_label = 'Select'
        self.fields['emp_code'].required = False
        self.fields['manager_name'].required = False

    def clean_phone_number(self):
        data = self.cleaned_data.get("phone_number")
        validator = RegexValidator('^[0-9]{3}-[0-9]{3}-[0-9]{4}$', "Phone Number format is 123-456-7890")
        if validator(data):
            raise forms.ValidationError("Incorrect format")
        return data
