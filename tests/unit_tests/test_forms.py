from django.test import TestCase

from purbeurre.accounts.forms import CustomAuthenticationForm


class CustomAuthenticationFormTest(TestCase):
    def test_authentication_form_password_field_label(self):
        form = CustomAuthenticationForm()
        # import pdb; pdb.set_trace()
        self.assertTrue(
            form.fields['password'].label == "Mot de passe"
            )
