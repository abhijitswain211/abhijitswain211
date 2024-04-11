from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from ecom import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode




# Create your views here.
def home(request):
    return render(request, "authentication\index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")  
            return redirect('home')  
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 characters")
            return redirect('home') 

        if pass1 != pass2:
            messages.error(request, "password didn't match!")
            return redirect('home') 

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('home')        


        myuser =  User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        messages.success(request,"Your Account has been sucessfully created. We have sent you a confirmation email, please confirm your email in order to activate your account. ")

        # welcome Email

        subject = "Welcome to STALLION!!"
        message = "Hello" + myuser.first_name + "!! \n" + "Welcome to STALLION! \n Thank you for visiting our website \n We have also sent you a email, Please confirm your email address in order to activate your account. \n\n Thank you"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        #Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm your email!"
        message2 = render_to_string('email_confirmation.html', {
            
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)


        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect("signin")
        
    return render(request, "authentication/signup.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError,OverflowError, User.DoseNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        
        messages.success(request, "Your Account has been activated!")

          
        return redirect('signin')
     
    else:
        return render(request, 'activation_failed.html')


def signin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        User = authenticate(username=username, password=pass1)

        if User is not None:
            login(request, User)
            fname = User.first_name
            messages.success(request, "Logged In Sucessfully!!")
            return render(request, "authentication/index.html", { 'fname': fname })

        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')
    return render(request, "authentication/signin.html")
            
   

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')


def shopnow(request):
    if request.method == 'POST':
        shop = request.POST.get('shop')

        return redirect('home')
    return render(request, "authentication\shopnow.html", {'shopnow.html' : 'shopnow/'})

        
def contactus(request):
    if request.method == 'POST':
        email = request.POST.get('Your email')
        message = request.POST.get('your message')
    
        return redirect('home')
    return render(request, "authentication\contactus.html")

def index(request):
    return HttpResponse('home')

    

