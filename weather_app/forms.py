from django import forms
from .models import Student, City 

class studentsform(forms.ModelForm):
  class Meta:
    model = Student
    fields =['name','age','roll_num','phone_num','email','address']

class CityForm(forms.ModelForm):
    
    class Meta:
        model = City
        fields = ['name']
        widgets ={
          'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'City Name'})
        }
