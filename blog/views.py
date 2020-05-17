from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Profile
import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Blog
from accounts.forms import ProfileUpdateForm


date=datetime.datetime.now()
date=date.strftime("%d")+'-'+date.strftime("%B")
if date[0]=='0':
   date=date[1:]
birth=Profile.objects.filter(dob__contains=date)


@login_required
def home(request):
    pro=Profile.objects.filter(user=request.user).first()
    blog=Blog.objects.all().order_by('-date')
    if request.method=='POST':
        b2=Blog()
        _, im=request.FILES.popitem()
        im=im[0]
        b2.profile=pro
        b2.content=request.POST['content']
        b2.image=im
        b2.save()
        return HttpResponseRedirect(reverse("home"))
    global birth
    c={'blog':blog,'pro':pro,'birth':birth}
    if request.method=='GET':
        sea=request.GET.get('s')
        if sea=="" or sea==None:
            pass
        else:
            u=User.objects.filter(first_name__istartswith=sea).all()
            s=Profile.objects.filter(user__in=u).all()
            c={'blog':blog,'pro':pro,'birth':birth,'se':s}
    return render(request,'blog/home.html',c)