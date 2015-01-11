from django.shortcuts import render
from accounts.models import Account 
from accounts.forms import createProfile,loginForm
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
import hashlib

# Create your views here.
def index(request):
    return render_to_response('index.html', context_instance = RequestContext(request))

def register(request):
  form = createProfile
  return render_to_response('register.html', {'form':form}, context_instance = RequestContext(request))

def save_details(request):
  form = createProfile(request.POST)
  if request.method == 'POST':
    if form.is_valid():
      username = form.cleaned_data['username']
      first_name= form.cleaned_data['first_name']
      last_name= form.cleaned_data['last_name']
      age = int(form.cleaned_data['age'])
      sex = form.cleaned_data['sex']
      location = form.cleaned_data['location']
      phone = int(form.cleaned_data['phone'])
      email = form.cleaned_data['email']
      unsafe_password=form.cleaned_data['password']
      password=hashlib.sha256(unsafe_password).hexdigest()
      profile = Account(username,first_name, last_name, age,sex,location,phone,email,password)
      profile.full_clean()
      profile.save()
      user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email)
      user.set_password(unsafe_password)
      user.save()
    else:
      message = 'Form has errors'
      return render_to_response('register.html', {'form':form,'message':message} , context_instance=RequestContext(request))
  form = loginForm()
  message = "profile is created.Log in to your profile"
  return render_to_response('login.html', {'message':message,'form':form}, context_instance = RequestContext(request))

def loginview(request):
  if request.method == 'GET':
    form = loginForm()
    return render_to_response('login.html', {'form':form} , context_instance=RequestContext(request))

  elif request.method == 'POST':
    form = loginForm(request.POST)
    if form.is_valid():
      print "form"
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
    else:
      message = 'Form has errors'
      return render_to_response('login.html', {'form':form,'message':message} , context_instance=RequestContext(request))
  try:
    user = Account.objects.get(username = username)
  except:
    message = 'user does not exist'
    return render_to_response('login.html', {'form':form,'message':message} , context_instance=RequestContext(request))
  if not user:
    message = 'Username/Password Incorrect or user does not exist'
    return render_to_response('login.html', {'form':form,'message':message} , context_instance=RequestContext(request))
  else:
    user_authenticate = authenticate(username=username, password=password)
    try:  
      login(request, user_authenticate)
    except:
      message = 'Could not authenticate!.Password Incorrect'
      return render_to_response('login.html', {'form':form,'message':message} , context_instance=RequestContext(request))
    
    if user.password == hashlib.sha256(password).hexdigest():
      return HttpResponseRedirect('/update/')
    else:
      message = 'Username/Password Incorrect'
      return render_to_response('login.html', {'form':form,'message':message} , context_instance=RequestContext(request))

def updateview(request):
    if request.user.is_authenticated:
	if request.method == 'GET':
	    print request.user
	    user_id=Account.objects.get(username=request.user)
	    data = {
		'username' : user_id.username,
		'first_name' : user_id.first_name,
		'last_name' : user_id.last_name,
		'age' : user_id.age,
		'sex' : user_id.sex,
		'location' : user_id.location,
		'phone' : user_id.phone,
		'email': user_id.email,
		'password' : user_id.password
		}
	    form = createProfile(data)
	    message='Fields with "Account with this Username already exists" should not be changed'
	    return render_to_response('update.html', {'form':form,'message':message}, context_instance = RequestContext(request))
	if request.method == 'POST':
	    form = createProfile(data=request.POST,instance=request.user)
	    if form.is_valid():
		username = form.cleaned_data['username']
		first_name= form.cleaned_data['first_name']
		last_name= form.cleaned_data['last_name']
		age = int(form.cleaned_data['age'])
		sex = form.cleaned_data['sex']
		location = form.cleaned_data['location']
		phone = int(form.cleaned_data['phone'])
		email = form.cleaned_data['email']
		password=form.cleaned_data['password']
		try:
		    profile =Account.objects.get(username=username)
		except:
		    message = 'Could not change the Username'
		    return render_to_response('update.html', {'form':form,'message':message} , context_instance=RequestContext(request))
		profile.first_name=first_name
		profile.last_name=last_name
		profile.age=age
		profile.sex=sex
		profile.location=location
		profile.phone=phone
		profile.password=hashlib.sha256(password).hexdigest()
		profile.full_clean()
		profile.save()
		user = User.objects.get(username=username)
		user.first_name=first_name
		user.last_name=last_name
		user.email=email
		user.set_password(password)
		user.save()
		message = 'form is Updated'
		return render_to_response('update.html', {'form':form,'message':message} , context_instance=RequestContext(request))
		
	    else:
		message = 'Form has error'
		return render_to_response('update.html', {'form':form,'message':message} , context_instance=RequestContext(request))
	    
	    
    else:
	message="Your not logged in. First try to log in"
	return render_to_response('login.html', {'form':form,'message':message} , context_instance=RequestContext(request))
	
def deleteview(request):
    account_id=Account.objects.get(username=request.user)
    account_id.delete()
    user_id=User.objects.get(username=request.user)
    user_id.delete()
    return HttpResponseRedirect('/register/')
    

def logoutview(request):
    logout(request)
    return HttpResponseRedirect('/login/')
    