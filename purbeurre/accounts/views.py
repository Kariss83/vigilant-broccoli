from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from purbeurre.accounts.forms import CustomUserCreationForm


# Create your views here.

# login view
def login_user(request):
	if request.method == 'POST':
		form = AuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(request, email=email, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, ('Vous êtes connecté(e)!'))
				return redirect('/')

			else:
				messages.success(request, (
					'Erreur de connexion - Veuillez reéssayer...'))
				return redirect('/login')
	else:
		return render(request, 'accounts/login.html', {})

# logout view
@login_required
def logout_user(request):
	logout(request)
	messages.success(request, ('Vous êtes déconnecté(e)...'))
	return redirect('/')

# register view
def register_user(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			email=form.cleaned_data['email']
			password = form.cleaned_data['password1']
			form.save()
			user = authenticate(email=email, password=password)
			print(user)
			if user is not None:
				login(request, user)
				messages.success(request, ('Vous êtes enregistré(e)...'))
				return redirect('/')
	else:
		form = CustomUserCreationForm()
	
	context = {'form': form}
	return render(request, 'registration/register.html', context)

# profile view
@login_required
def profile(request):
	return render(request, 'registration/profile.html', {})
