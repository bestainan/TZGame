# coding=utf-8
# Created by TTc9082 on 12/16/14
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.db.models import Q
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm

from exception.user_error import UserHasExist, TelRequire, TelNumberError, PasswordRequire, BankCardRequire, CardNameRequire, BankNameRequire, ALiPayNameRequire, ALiPayAccountRequire, PasswordsDifferent, UserDoesNotExist, InviteUserDoesNotExist, CaptchaError, CaptchaExpire
from tz_user.models import TZUser, Mail
from tz_user.utils import check_phone


class SignUpForm(forms.Form):
    tel = forms.CharField(max_length=11, required=False)
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    captcha = forms.IntegerField(required=False)
    invite_code = forms.IntegerField(required=False)

    class Meta:
        model = TZUser
        fields = ['tel', 'captcha', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SignUpForm, self).__init__(*args, **kwargs)

    def clean_tel(self):
        tel = self.cleaned_data['tel']
        if not tel:
            raise TelRequire()
        if not check_phone(tel):
            raise TelNumberError(0)
        user = TZUser.objects.filter(tel=tel).first()
        if user:
            raise UserHasExist()
        return tel

    def clean_captcha(self):
        session_v_code = self.request.session.get('v_code')
        if not session_v_code:
            raise CaptchaExpire()

        if self.cleaned_data['captcha'] != session_v_code:
            raise CaptchaError()

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if not password1:
            raise PasswordRequire()
        return password1

    def clean_password2(self):
        if self.cleaned_data.get('password1', ''):
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 != password2:
                raise PasswordsDifferent()

    def save(self):
        from django.contrib.auth.models import User
        user_name = self.cleaned_data['tel']
        password = self.cleaned_data['password1']
        invite_code = self.cleaned_data['invite_code']

        auth_user = User.objects.create_user(username=user_name)
        auth_user.set_password(password)
        auth_user.save()
        q = {
            "auth": auth_user,
            "tel": user_name,
        }
        if invite_code:
            invite_user = TZUser.objects.filter(invite_code=invite_code).fitst()
        q["invite_user"] = invite_user


        user =  TZUser.objects.create(**q)
        auth_user = authenticate(username=user_name, password=password)
        login(self.request, auth_user)
        Mail.objects.create(
            title='欢迎',
            info='欢迎来到王者挑战赛',
            user=user
        )
        return user



class ForgetPasswordForm(forms.Form):
    tel = forms.CharField(max_length=11, required=False)
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    captcha = forms.IntegerField(required=False)


    class Meta:
        model = TZUser
        fields = ['tel', 'captcha', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ForgetPasswordForm, self).__init__(*args, **kwargs)

    def clean_tel(self):
        tel = self.cleaned_data['tel']
        if not tel:
            raise TelRequire()
        if not check_phone(tel):
            raise TelNumberError()
        self.user = TZUser.objects.filter(tel=tel).first()
        if not self.user:
            raise UserDoesNotExist()
        return tel

    def clean_captcha(self):
        session_v_code = self.request.session.get('v_code')
        if not session_v_code:
            raise CaptchaExpire()

        if self.cleaned_data['captcha'] != session_v_code:
            raise CaptchaError()

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if not password1:
            raise PasswordRequire()
        return password1

    def clean_password2(self):
        if self.cleaned_data.get('password1', ''):
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 != password2:
                raise PasswordsDifferent()

    def save(self):
        password = self.cleaned_data['password1']
        self.user.auth.set_password(password)
        self.user.auth.save()

        return self.user