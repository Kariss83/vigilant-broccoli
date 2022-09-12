from django.test import TestCase

from purbeurre.accounts.forms import (
    CustomAuthenticationForm,
    CustomUserChangeForm,
    CustomPasswordResetForm,
)


class CustomAuthenticationFormTest(TestCase):
    def test_authentication_form_password_field_label(self):
        form = CustomAuthenticationForm()
        # import pdb; pdb.set_trace()
        self.assertTrue(form.fields["password"].label == "Mot de passe")


class CustomeUserChangeForm(TestCase):
    def test_user_change_form_password_fields_label(self):
        form = CustomUserChangeForm()
        self.assertTrue(form.fields["name"].label == "Nom")
        self.assertTrue(form.fields["email"].label == "Adresse Mail")


class CustomAuthenticationFormTest(TestCase):
    def test_authentication_form_password_field_label(self):
        form = CustomPasswordResetForm()
        # import pdb; pdb.set_trace()
        self.assertTrue(form.fields["email"].label == "Email")
