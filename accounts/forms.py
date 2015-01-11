from django import forms
from django.forms import ModelForm
from accounts.models import Account
sex_choices = (
      ('Male','Male'),
      ('Female','Female'),
    )

class loginForm(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput())
 
class createProfile(ModelForm):
  '''
  username = forms.CharField(max_length=100)
  first_name = forms.CharField(max_length=100,blank=True)
  last_name = forms.CharField(max_length=100,blank=True)
  email = forms.EmailField()
  age = forms.IntegerField()
  sex = forms.ChoiceField(choices=sex_choices,label = 'Sex')
  location = forms.CharField(max_length=100)
  phone = forms.IntegerField()
  password = forms.CharField(widget=forms.PasswordInput())
  '''
  sex = forms.ChoiceField(choices=sex_choices,label = 'Sex')
  password = forms.CharField(widget=forms.PasswordInput())
  class Meta:
    model = Account
    fields = ['username','first_name', 'last_name', 'email','age','sex','location','phone','password']
