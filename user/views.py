from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
import random
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .token import activation_token
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from .serializers import UserLocationSerializer
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt

account_sid = "AC9290a81e9e019044728d85eb4365b16a"
auth_token = "7419c359fe27d873c0cd2751d027f784"
client = Client(account_sid, auth_token)

# Create your views here.

def login_user(request):
    context = {}
    if request.user.is_authenticated:
        return redirect("/home")
    else: 
        validation = ""
        if request.method == "POST":
            phone = request.POST['phone']
            try:
                user = CustomUser.objects.get(Q(phone_number=int(phone)) & Q(is_active=True))
                mail_subject = "KitchenAroma Login"
                # html_message = render_to_string('signup_template.html', {'user': user})
                # plain_message = strip_tags(html_message)
                # to_email = email
                # to_list = [to_email]
                # from_email = settings.EMAIL_HOST_USER
                # send_mail(mail_subject, plain_message, from_email, to_list, html_message=html_message, fail_silently=True)
                messages = client.messages.create(
                     body="Your OTP is: " + str(user.verfication_code) + "." + "\n" + "@kitchenaroma.co.in #" + str(user.verfication_code),
                     from_='+18705282231',
                     to= '+91' + str(user.phone_number)
                 )
                return redirect("/login_validate/" + str(user.id))
            except:
                validation = "User with phone " + str(phone) + " does not exist"
                context["message"] = validation
    return render(request, 'login.html', context)


@csrf_exempt
def login_validate(request, pk):
    error_message = ""
    if request.method == "POST":
        if request.POST["otp"] != "":
            user = CustomUser.objects.get(id=pk)
            verfication_code = user.verfication_code
            if int(request.POST['otp']) == verfication_code:
                login(request, user)
                new_verfication_code = random.randint(1111,9999)
                user.verfication_code = new_verfication_code
                user.save()
                return redirect("/")
            else:
                error_message = "Invalid OTP"
        else:
            error_message = "Please enter a valid OTP"
    return render(request, "login_validate.html", {"error": error_message})


def register(request):
    message = ""
    if request.method == "POST":
        full_name = request.POST['full_name']
        # email = request.POST['email']
        phone = request.POST['phone']
        try:
            user_exist = CustomUser.objects.get(phone_number=phone)
            message = "Account with phone " + str(phone) + " already exist"
        except:
            if len(phone) != 10:
                message = "Invalid phone number"
            else:
                user = CustomUser()
                user.first_name = full_name
                # user.email = email
                user.phone_number = phone
                user.is_active = False
                user.save()
                # mail_subject = "KitchenAroma Profile Activation"
                # html_message = render_to_string('activation_template.html', {
                #     "user": user,
                #     'id': user.id,
                #     'token': activation_token.make_token(user)
                # })
                # plain_message = strip_tags(html_message)
                # to_email = email
                # to_list = [to_email]
                # from_email = settings.EMAIL_HOST_USER
                acc_activation_code = random.randint(1111,9999)
                user.verfication_code = acc_activation_code
                user.save()
                # send_mail(mail_subject, plain_message, from_email, to_list, html_message=html_message, fail_silently=True)
                # message = "You will receive an email with your account activation link"
            
                messages = client.messages.create(
                     body="Your OTP is: " + str(acc_activation_code) + "." + "\n" + "@kitchenaroma.co.in #" + str(acc_activation_code),
                     from_='+18705282231',
                     to= '+91' + str(phone)
                )
                return redirect(otp_validation)     
    return render(request, 'register.html', {'message': message})


@csrf_exempt
def otp_validation(request):
    error_message = ""
    if request.method == "POST":
        if request.POST["otp"] != "":
            try:
                user = CustomUser.objects.get(verfication_code=request.POST["otp"])
                user.is_active = True
                user.save()
                login(request, user)
                return redirect("/")
            except:
                error_message = "Invalid OTP"
            else:
                error_message = "Invalid OTP"
        else:
            error_message = "Please enter a valid OTP"
    return render(request, 'otp-validation.html', {"error": error_message})    


def account_activation(request, id, token):
    try:
        user = get_object_or_404(CustomUser, pk=id)
    except:
        raise Http404("User not found")
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'after_activation.html')
    else:
        return render(request, 'activation_error.html')


class UserLocationAPIView(APIView):
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        UserDetails = UserLocationSerializer(obj, context={"request": request})
        return Response(UserDetails.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = UserLocationSerializer(obj, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)          
