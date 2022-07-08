# from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages #import messages

from accounts.models import CustomUser
from accounts.forms import CustomPasswordResetForm


# Create your views here.
class HomeView(TemplateView):
	template_name = 'home/index.html'


class LegalView(TemplateView):
	template_name = "home/legal.html"

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = CustomPasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = CustomUser.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "passwords/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					# return redirect ("/password_reset/done/")
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ('home:home')
			messages.error(request, 'An invalid email has been entered.')
	password_reset_form = CustomPasswordResetForm()
	return render(request=request, template_name="passwords/password_reset.html", context={"password_reset_form":password_reset_form})