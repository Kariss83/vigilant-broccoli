from django import forms as test_form
from django.contrib.auth import forms, password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from purbeurre.accounts.models import CustomUser


# class CustomUserCreationForm(forms.UserCreationForm):
#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
#     password1 = test_form.CharField(widget=test_form.PasswordInput(attrs={
#                                     'class':'form-control', 
#                                     'placeholder':'Mot de Passe'}))
#     password2 = test_form.CharField(widget=test_form.PasswordInput(attrs={
#                                     'class':'form-control', 
#                                     'placeholder':'Confirmez le Mot de Passe'}))

#     class Meta(forms.UserCreationForm.Meta):
#         model = CustomUser
#         fields = ('email',)

#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Les mots de passe diffèrent.")
#         return password2

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user



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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format("../password/")
        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                "content_type"
            )




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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return 