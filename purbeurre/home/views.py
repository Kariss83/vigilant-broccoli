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
from django.contrib import messages  # import messages

from purbeurre.accounts.models import CustomUser
from purbeurre.accounts.forms import CustomPasswordResetForm


# Create your views here.
class HomeView(TemplateView):
    template_name = "home/index.html"


class LegalView(TemplateView):
    template_name = "home/legal.html"


# password reset request view
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = CustomPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "passwords/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "PurBeurre",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "root@vps-8351387e.vps.ovh.net",
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    messages.success(
                        request,
                        "Un message contenant les instructions de réinitialisation vous a été envoyé.",
                    )
                    return redirect("home:home")
            else:
                messages.error(request, "Cet email est invalide.")
                return redirect("/password_reset")
    else:
        password_reset_form = CustomPasswordResetForm()
        return render(
            request,
            "passwords/password_reset.html",
            {"password_reset_form": password_reset_form},
        )
