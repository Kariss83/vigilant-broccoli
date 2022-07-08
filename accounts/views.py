from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode

from accounts.forms import (
	CustomUserCreationForm,
	CustomAuthenticationForm,
	CustomUserChangeForm
)


# Create your views here.

# login view
def login_user(request):
	# import pdb; pdb.set_trace()
	if request.method == 'POST':
		# import pdb; pdb.set_trace()
		form = CustomAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST.get('username', '')
			password = request.POST.get('password', '')
			user = authenticate(request, email=email, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, ('Vous êtes connecté(e)!'))
				return redirect('/')
			else:
				messages.error(
					request,
					('Erreur de connexion - Veuillez reéssayer...')
					)
				return redirect('/users/login')
		else:
			messages.error(request, (
				'Erreur de connexion - Veuillez reéssayer...'))
			return redirect('/users/login')
	else:
		return render(
			request,
			'registration/login.html',
			{'form': CustomAuthenticationForm()}
			)


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
			email = form.cleaned_data['email']
			password = form.cleaned_data['password1']
			form.save()
			user = authenticate(email=email, password=password)
			# import pdb; pdb.set_trace()
			if user is not None:
				login(request, user)
				messages.success(request, ('Vous êtes enregistré(e)...'))
				return redirect('/')
		else:
			messages.error(request, (
				'Erreur de Création de Comptes - Veuillez reéssayer...'))
			return redirect('/users/register')
	else:
		form = CustomUserCreationForm()
		context = {'form': form}
		return render(
			request,
			'registration/register.html',
			context
			)


# profile view
@login_required
def profile(request):
	return render(request, 'accounts/profile.html', {})

	
# edit profile view
@login_required
def edit_profile(request):
	if request.method == 'POST':
		# import pdb; pdb.set_trace()
		form = CustomUserChangeForm(request.POST, instance=request.user)
		if form.is_valid():
			email = form.data['email']
			name = form.data['name']
			form.save()
			messages.success(request, ('Modifications enregistrées avec succès.'))
			return redirect('/')
		else:
			messages.error(request, (
				'Erreur de modification des informations, le formulaire n\'est pas valide'))
			return redirect('/users/edit')
	else:
		form = CustomUserChangeForm(instance= request.user)
		context = {'form': form}
		return render(
			request,
			'accounts/edit_profile.html',
			context
			)