# coding=utf-8
# Created by TTc9082 on 12/16/14
from django.contrib.sessions.models import Session
from django.db.models import Q
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm

from exception.user_error import UserHasExist, TelRequire, TelNumberError, PasswordRequire, BankCardRequire, CardNameRequire, BankNameRequire, ALiPayNameRequire, ALiPayAccountRequire, PasswordsDifferent, UserDoesNotExist, InviteUserDoesNotExist
from tz_user.models import TZUser
from tz_user.utils import check_phone


class SignUpForm(forms.Form):
    tel = forms.CharField(max_length=11, required=False)
    nickname = forms.CharField(required=False)
    invite_code = forms.CharField(required=False)
    # captcha = forms.CharField(max_length=4, required=True)
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    bank_type = forms.CharField(required=False)

    class Meta:
        model = TZUser
        fields = ['tel', 'nickname', 'captcha', 'password1', 'password2']

    def clean_bank_type(self):
        bank_type = self.cleaned_data['bank_type']
        if bank_type == 'bank':
            if not self.data.get('card_name'):
                raise CardNameRequire()
            if not self.data.get('card_account'):
                raise BankCardRequire()
            if not self.data.get('bank_name'):
                raise BankNameRequire()
        else:
            if not self.data.get('alipay_name'):
                raise ALiPayNameRequire()
            if not self.data.get('alipay_account'):
                raise ALiPayAccountRequire()

    def clean_tel(self):
        tel = self.cleaned_data['tel']
        if not tel:
            raise TelRequire()
        if not check_phone(tel):
            raise TelNumberError(0)
        if TZUser.objects.filter(tel=tel):
            raise UserHasExist()
        return tel

    #
    # def clean_captcha(self):
    #     session_captcha = self.request.session.get('verification_num', 100)
    #     captcha = self.cleaned_data['captcha']
    #     if 6 <= len(str(captcha)) < 5:
    #         raise forms.ValidationError(u'验证码是5位。')
    #     if str(session_captcha) != str(captcha):
    #         raise forms.ValidationError(u'验证码错误。')
    #
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

    def save(self, commit=True):
        from django.contrib.auth.models import User
        user_name = self.cleaned_data['tel']
        password = self.cleaned_data['password1']
        nickname = self.cleaned_data['nickname']
        bank_type = self.data['bank_type']

        auth_user = User.objects.create_user(username=user_name)
        auth_user.set_password(password)
        auth_user.save()
        q = {
            "auth": auth_user,
            "nickname": nickname,
            "tel": user_name,
        }
        if self.cleaned_data['invite_code']:
            invite_user = TZUser.objects.filter(invite_code=self.cleaned_data['invite_code']).first()
            if invite_user:
                q['invite_user'] = invite_user
            else:
                raise InviteUserDoesNotExist()
        if bank_type == 'bank':
            q['bank_card_name'] = self.data.get('card_name')
            q['bank_account'] = self.data.get('card_account')
            q['bank_name'] = self.data.get('bank_name')
        else:
            q['alipay_name'] = self.data.get('alipay_name')
            q['alipay_account'] = self.data.get('alipay_account')
        while 1:
            try:
                tz_user = TZUser.objects.create(**q)
                break
            except:
                continue
        Session.objects.filter(session_key=user_name).delete()
        return tz_user
