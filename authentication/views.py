from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from propertiesPrediction import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.core.mail import EmailMessage, send_mail

# Create your views here.

def home(request):
    return render(request, 'home/index.html')

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        conf_password = request.POST['conf_password']
        
        if User.objects.filter(username=name):
            messages.error(request, "Username already exist! please try some other username.")
            return redirect('register')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registred!")
            return redirect('register')
        
        if len(name) > 15:
            messages.error(request, "Username must be under 15 characters.")
            return redirect('register')
            
        if password != conf_password:
            messages.error(request, "Password did not match!")
            return redirect('register')
            
        if not name.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('register')
        
        user = User.objects.create_user(name, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.is_active = False
        user.save()
        
        messages.success(request, "Your accoubt has been successfully created. We have sent you a confirmation email, please confirm you email in order to complete your registration.")
        
        # Welcome Email
        subject = "Welcome to MaFutuSight."
        message = "Hello " + user.first_name + "\n" + "Thank you for visiting MaFutuSight.\nWe have also sent you a confirmation, please confirm your email address in order to activate your account.\n\nMaFutuSight. Team"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        """ uid = urlsafe_base64_encode(force_bytes(user.pk))
        print(uid)
        
        token = generate_token.make_token(user)
        print(token) """
        
        # Email Confirmation
        current_site = get_current_site(request)
        email_subject = "Confirm your email address\n\nMaFutuSight."
        message2 = render_to_string('email_confirmation.html', {
            'name': user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),
        })
        
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.fail_silently = False
        email.send()
        
        messages.success(request, "Your account has been created successfully.")
        return redirect('connection')
    return render(request, 'authentication/registerPage.html')

def connection(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            firstname = user.first_name
            messages.success(request, "Your are now logged in.")
            return render(request, "main/predictionPage.html", {'firstname': firstname})
        else:
            messages.error(request, "You entred a wrong informations, check again...")
            return redirect('connection')
    return render(request, 'authentication/connectionPage.html')

def signout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully!!")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation_failes.html')