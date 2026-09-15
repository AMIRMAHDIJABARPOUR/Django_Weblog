from django import forms
from .models import Contact, Newsletter
from captcha.fields import CaptchaField


class ContactModelForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Contact
        fields = "__all__"
        exclude = ("created_date",)


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        exclude = ("joined_date",)
        fields = ("email",)
