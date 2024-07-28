import random

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views import View

from apps.accounts.forms import UserRegisterForm, VerifyOtpCodeForm
from apps.accounts.models import OtpCode, User
from apps.utils.otp import send_otp_code


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_otp = random.randint(1000, 9999)
            send_otp_code(cd['phone'], random_otp)
            OtpCode.objects.create(phone_number=cd['phone'], code=random_otp)

            # save user info in session
            request.session['user_registration_info'] = {
                'phone_number': cd['phone'],
                'email': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password']
            }
            messages.success(request, 'we send you otp code', extra_tags='success')
            return redirect('accounts:verify_otp_code')
        return render(request, self.template_name, {'form': form})


class UserVerifyOtpView(View):
    form_class = VerifyOtpCodeForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session.get('user_registration_info')
        code_instance = OtpCode.objects.get(phone_number=user_session.get('phone_number'))

        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            otp_code = cd['code']

            if otp_code == code_instance.code:
                user = User.objects.create_user(phone_number=user_session.get('phone_number'),
                                                email=user_session.get('email'),
                                                full_name=user_session.get('full_name'),
                                                password=make_password(user_session.get('password')))
                code_instance.delete()
                login(request, user)
                messages.success(request, 'you registered', extra_tags='success')
                return redirect('home:home')
            else:
                messages.error(request, 'wrong otp code', extra_tags='danger')
                return redirect('accounts:verify_otp_code')
        return redirect('home:home')
