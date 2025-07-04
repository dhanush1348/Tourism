from allauth.account.adapter import DefaultAccountAdapter
from .forms import CustomSignupForm

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_signup_form_class(self):
        return CustomSignupForm 