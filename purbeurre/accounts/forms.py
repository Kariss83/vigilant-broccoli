from django import forms as test_form
from django.contrib.auth import forms, password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from purbeurre.accounts.models import CustomUser


class CustomAuthenticationForm(test_form.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """

    username = test_form.EmailField(
        widget=test_form.TextInput(attrs={"autofocus": True})
        )
    password = test_form.CharField(
        label=_("Mot de passe"),
        strip=False,
        widget=test_form.PasswordInput(attrs={"autocomplete": "current-password"}),
        )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }


class CustomUserChangeForm(forms.UserChangeForm):
    password = forms.ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta(forms.UserChangeForm.Meta):
        model = CustomUser
        fields = "__all__"
        field_classes = {"username": forms.UsernameField}


class CustomUserCreationForm(forms.UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    password1 = test_form.CharField(
        label=_("Mot de Passe"),
        strip=False,
        widget=test_form.PasswordInput(attrs={
                                        "autocomplete": "new-password",
                                        "class" : "form-control",
                                        "placeholder": "Mot de Passe",
                                        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = test_form.CharField(
        label=_("Confirmation du Mot de Passe"),
        widget=test_form.PasswordInput(attrs={
                                        "autocomplete" : "new-password",
                                        "class" : "form-control",
                                        "placehoder" : "Confirmez le Mot de Passe",
                                        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta(forms.UserChangeForm.Meta):
        model = CustomUser
        fields = ("email", "name")
        field_classes = {"email": forms.UsernameField}