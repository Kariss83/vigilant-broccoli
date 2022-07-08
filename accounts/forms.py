from django import forms as base_form
from django.contrib.auth import forms
from django.utils.translation import gettext_lazy as _


from accounts.models import CustomUser


class CustomAuthenticationForm(base_form.Form):
	"""
	Base class for authenticating users. Extend this to get a form that accepts
	username/password logins.
	"""

	username = base_form.EmailField(
		widget=base_form.TextInput(attrs={"autofocus": True})
		)
	password = base_form.CharField(
		label=_("Mot de passe"),
		strip=False,
		widget=base_form.PasswordInput(attrs={"autocomplete": "current-password"}),
		)

	error_messages = {
		"invalid_login": _(
			"Please enter a correct %(username)s and password. Note that both "
			"fields may be case-sensitive."
		),
		"inactive": _("This account is inactive."),
	}


class CustomUserChangeForm(forms.UserChangeForm):
	"""
	A form to allow modification of the profile email adress and name.
	"""
	name = base_form.CharField(max_length=100,
                           required=True,
                           widget=base_form.TextInput(
							attrs={'class': 'form-control'})
						  )
	email = base_form.EmailField(required=True,
                             widget=base_form.TextInput(
								attrs={'class': 'form-control'})
							)
	password = None
	class Meta(forms.UserChangeForm.Meta):
		model = CustomUser
		fields = ("email", "name")
		field_classes = {"email": forms.UsernameField}


class CustomUserCreationForm(forms.UserCreationForm):
	"""
	A form that creates a user, with no privileges, from the given email and
	password.
	"""

	error_messages = {
		"password_mismatch": _("The two password fields didn’t match."),
	}
	password1 = base_form.CharField(
		label=_("Mot de Passe"),
		strip=False,
		widget=base_form.PasswordInput(attrs={
										"autocomplete": "new-password",
										"class": "form-control",
										"placeholder": "Mot de Passe",
										}),
		help_text="",
	)
	password2 = base_form.CharField(
		label=_("Confirmation du Mot de Passe"),
		widget=base_form.PasswordInput(attrs={
										"autocomplete": "new-password",
										"class": "form-control",
										"placehoder": "Confirmez le Mot de Passe",
										}),
		strip=False,
		help_text="",
	)

	class Meta(forms.UserChangeForm.Meta):
		model = CustomUser
		fields = ("email", "name")
		field_classes = {"email": forms.UsernameField}
