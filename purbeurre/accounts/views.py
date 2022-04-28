from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages 
from purbeurre.forms import CustomUserCreationForm



# # Create your views here.
# def login_user(request):
# 	if request.method == 'POST':
# 		form = LoginForm(request.POST)
# 		if form.is_valid():
# 			email = request.POST['username']
# 			password = request.POST['password']
# 			user = authenticate(request, email=email, password=password)
# 			if user is not None:
# 				login(request, user)
# 				messages.success(request, ('Vous êtes connecté(e)!'))
# 				return redirect('/')

# 			else:
# 				messages.success(request, ('Erreur de connexion - Veuillez reéssayer...'))
# 				return redirect('/login')
# 	else:
# 		return render(request, 'users/login.html', {})

# def logout_user(request):
# 	logout(request)
# 	messages.success(request, ('Vous êtes déconnecté(e)...'))
# 	return redirect('/')

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
	return render(request, 'users/register.html', context)