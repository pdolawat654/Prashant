from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
import datetime
from django.core.mail import send_mail
import random
import requests

URL = 'https://www.sms4india.com/api/v1/sendCampaign'

def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  'senderid':senderId
  }
  requests.post(reqUrl, req_params)


date=datetime.datetime.now()
date=date.strftime("%d")+'-'+date.strftime("%B")
if date[0]=='0':
    date=date[1:]
birth=Profile.objects.filter(dob__contains=date)

def register(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['password1']
        pass2=request.POST['password2']
        phone=request.POST['phone']
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                messages.info(request,"Email Id already Exists!")
                return redirect('register')
            else:
                user=User.objects.create_user(first_name=fname,last_name=lname,username=email,password=pass1,email=email)
                o=str(random.randint(100000,999999))
                pro=Profile(user=user,phone=phone,otp=o)
                pro.save()
                m='Hey '+fname+'!\n'+'Thank you for registering with the JNEC ALUMNI CELL!\n\n'+'Your OTP is :'+o
                send_mail('Registration Successful!',m,'J.N.E.C ALumni Cell',[email],fail_silently=True)
                sendPostRequest(URL, '9DP4N6S7J555W4TWM72E5X10E8FM6Z04', '7L5JPGHL49QZAWTK', 'prod', phone, 'JNECAL', m )
                messages.info(request,"Account Created Successfully")
                return redirect('login')
        else:
            messages.info(request,"Passwords didn't matched!")
            return redirect('register')
    else:
        return render(request,'accounts/register.html')
def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(username=email,password=password)
        if user is not None:
            auth.login(request, user)
            pro=Profile.objects.filter(user=user).first()
            if pro.verify=='0':
                return redirect('verify')
            else:
                return redirect('uprofile')
        else:
            messages.info(request,"Invalid Credentials!")
            return redirect('login')
    else:
        return render(request,'accounts/login.html')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def uprofile(request):
    years=[]
    d=[]
    y=[]
    for x in range(1950,2021):
        y.append(x)
    for x in range(1,32):
        d.append(x)
    for x in range(1980,2021):
        years.append(x)
    pro=Profile.objects.filter(user=request.user).first()
    if request.method=='POST':
        try:
            _, file = request.FILES.popitem()
            file = file[0]
            pro.image = file
        except:
            pass
        finally:
            pro.phone=request.POST['phone']
            da=request.POST['d']
            mo=request.POST['m']
            ye=request.POST['y']
            dob=da+"-"+mo+"-"+ye
            pro.dob=dob
            pro.branch=request.POST['branch']
            pro.workat=request.POST['work']
            pro.passout=request.POST['passout']
            pro.save()
            return redirect('home')
    global birth
    c={'pro':pro,'years':years,'birth':birth,'d':d,'y':y}
    if request.method=='GET':
        sea=request.GET.get('s')
        if sea=="" or sea==None:
            pass
        else:
            u=User.objects.filter(first_name__istartswith=sea).all()
            s=Profile.objects.filter(user__in=u).all()
            c={'years':years,'d':d,'y':y,'birth':birth,'pro':pro,'se':s}
    return render(request,'accounts/uprofile.html',c)


@login_required
def profile(request):
    pro=Profile.objects.filter(user=request.user).first()
    global birth
    c={'pro':pro,'birth':birth}
    if request.method=='GET':
        sea=request.GET.get('s')
        if sea=="" or sea==None:
            pass
        else:
            u=User.objects.filter(first_name__istartswith=sea).all()
            s=Profile.objects.filter(user__in=u).all()
            c={'pro':pro,'se':s,'birth':birth}
    return render(request,'accounts/profile.html',c)

@login_required
def verify(request):
    pro=Profile.objects.filter(user=request.user).first()
    if request.method=='POST' and request.POST.get('submit1')=='Submit':
        o=request.POST['otp']
        if pro.otp==o:
            pro.verify='1'
            pro.save()
            return redirect('uprofile')
        else:
            messages.info(request,"Invalid OTP!")
            return redirect('verify')
    elif request.method=='POST' and request.POST.get('resend')=='Resend OTP':
        o=str(random.randint(100000,999999))
        fname=pro.user.first_name
        email=pro.user.username
        pro.otp=o
        pro.save()
        m='Hey '+fname+'!\n'+'Thank you for registering with the JNEC ALUMNI CELL!\n\n'+'Your OTP is :'+o
        send_mail('Registration Successful!',m,'J.N.E.C ALumni Cell',[email],fail_silently=True)
        return redirect('verify')
    return render(request,'accounts/verify.html')