from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from .forms import RegisterationFrom
from .models import Account


# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .token import account_activation_token


def register(request):
    if request.method == "POST":
        form = RegisterationFrom(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['Phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.Phone_number = phone_number
            #user.is_active = True
            user.save()
            
            
            # USER ACTIVATION
            current_site = get_current_site(request)
            subject = 'Please activate your account'
            message = render_to_string('home/accounts/email_activate/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(subject, message, to=[to_email])
            send_email.send()
            
            # messages.success(request, 'Check Gmail To Active Your Account')
            return redirect('/accounts/login/?command=verification&email='+email)

    else:
        form = RegisterationFrom()

    context={
        'forms':form,
    }
    return render(request, 'home/accounts/register.html',context)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Your email or password is wrong!')
            return redirect('accounts:login')

    return render(request, 'home/accounts/login.html')


@login_required(login_url = 'accounts:login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You've successfully logged out . Come back soon!")
    return redirect('accounts:login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is activated, log in and let's go.")
        return redirect('accounts:login')
    else:
        messages.error(request, "Invalid activation link, Try again!")
        return redirect('accounts:register')


@login_required(login_url = 'accounts:login')
def dashboard(request):
    context={

    }
    return render(request, 'home/accounts/dashboard/dashboard.html', context)


def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
            # SEND EMAIL
            current_site = get_current_site(request)
            subject = 'Reset Your Password'
            message = render_to_string('home/accounts/forget_password/send_resetpassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(subject, message, to=[to_email])
            send_email.send()

            # essages.success(request, "We sent a verification message to your email, click verify it, and let's start")
            
            
            return redirect('/accounts/forget_password/?command=resetpassword&email='+email)
        else: 
            messages.error(request, 'This email does not exist!')
            return redirect('accounts:forget_password')

    return render(request, 'home/accounts/forget_password/forget_password.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        request.session['uid'] = uid
        return redirect('accounts:reset_password')
    else:
        messages.error(request, 'This is link has been expired !')
        return redirect('accounts:forget_password')



def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        repeat_password = request.POST['confirm_password']

        try:
            if password == repeat_password:
                uid = request.session.get('uid')
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password Reset Successful')
                return redirect('accounts:login')
            else:
                messages.error(request, "Password does not match!")
                return redirect('accounts:reset_password')
        except Account.DoesNotExist:
            messages.error(request, "Please enter your email address here first! ")
            return redirect('accounts:forget_password')

    else:
        return render(request, 'home/accounts/forget_password/reset_password.html')