from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
sex_choices = (
      ('Male','Male'),
      ('Female','Female'),
    )

class Account(models.Model):
  username = models.CharField(max_length=100,unique=True,primary_key=True)
  first_name = models.CharField(max_length=100,blank=True)
  last_name = models.CharField(max_length=100,blank=True)
  age = models.IntegerField(max_length=3,validators=[RegexValidator(regex='^\d{2}$', message='Length has to be 2 or 3', code='Invalid number')])
  sex = models.CharField(max_length=10,choices=sex_choices)
  location = models.CharField(max_length=100)
  phone = models.CharField(max_length=10, validators=[RegexValidator(regex='^\d{10}$', message='Length has to be 10', code='Invalid number')])
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=100)

  def __unicode__(self):
      return self.username