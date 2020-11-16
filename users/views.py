from django.shortcuts import render,redirect
from django.contrib import messages
# DELETED -->from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
# importing Model forms	i.e UserUpdateForm, ProfileUpdateForm above


# Create your views here.
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f'Your account has been created! You are now able to log in')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html',{'form':form})

@login_required
def  profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, 
									request.FILES,
								 	instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request,f'Your account has been updated!')
			return redirect('profile')
			# we are returning here because of "POST GET REDIRECT PATTERN"
			# sometimes we have seen, after submitting a form if we reload
			# it gives a warning like " are you sure u want to resubmit the form because the form will be resubmitted"
			# This means the browser is telling you that it is going to make another POST REQUEST
			# when you reload the page
			# SO here with [redirect('profile')] request we are making a GET REQUEST
			# and we will not get that weired message
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	#we need to pass these forms in template so we need context
	# context is a dictionary
	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request,'users/profile.html', context)
