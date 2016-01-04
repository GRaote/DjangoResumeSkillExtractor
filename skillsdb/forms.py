from django import forms
#from ems.models import Employee
from django.db import models
import datetime
from django.core.exceptions import ValidationError
'''class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=40, help_text="First Name : ")
    last_name = forms.CharField(max_length=40, help_text="Last Name : ")
    phone_extension = forms.IntegerField(help_text="Phone Extension : ",initial=0)
    location = forms.CharField(max_length=30, help_text="Location : ")
    email = forms.CharField(max_length=100, help_text="Email : ")
    date_of_birth = forms.DateField(help_text="Date of Birth : ")
    employee_status = forms.ChoiceField(choices=((1, 'Active'), (0, 'Inactive')), help_text="Status : ")
    confirm_add = forms.IntegerField(widget=forms.HiddenInput(), initial=-1)
    class Meta:
        model = Employee
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if (date_of_birth > datetime.date.today()) or (date_of_birth == datetime.date.today()):
            raise forms.ValidationError("The date cannot be today or in future!")
        return date_of_birth  '''

'''class UploadFileForm(forms.Form):
    #file1 = forms.FileField(help_text="Upload .pdf or .docx Files only")
    file2 = forms.FileField(help_text="Upload Skills.xlsx File")'''
    
class UploadFileForm(forms.Form):
    candidate_name = forms.CharField(help_text ='Enter Candidate\'s full name')

    file1 = forms.FileField(
        label='Select a file',
        help_text='Upload .pdf or .docx Files only' )
    file2 = forms.FileField(help_text="Upload Skills.xlsx File")
