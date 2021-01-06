# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from user.models import CustomUser
from django.db.models import Q
from base.models import Kitchen, Category
from base.forms import KitchenForm, CategoryForm
from django.http import HttpResponseRedirect

@login_required(login_url="/login_adminkitchen")
def index(request):
    user = request.user
    kitchen = Kitchen.objects.get(user=user)
    return render(request, 'index_admin.html', {"kitchen": kitchen})

@login_required(login_url="/login_adminkitchen")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))


def login_adminkitchen(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = CustomUser.objects.get(Q(username=username) & Q(password=password))
            if user is not None and user.is_staff==True:
                login(request, user)
                return redirect("/adminkitchen")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})


def logout_adminkitchen(request):
    logout(request)
    return redirect('/login_adminkitchen')


@login_required(login_url="/login_adminkitchen")
def kitchen_adminview(request):
    user = request.user
    kitchen = Kitchen.objects.get(user=user)

    if request.method == "POST":
        kitchen.about = request.POST["about"]
        kitchen.contact = request.POST["contact"]
        kitchen.address_line_1 = request.POST["address_line_1"]
        kitchen.address_line_2 = request.POST["address_line_2"]
        kitchen.fb_link = request.POST["fb_link"]
        kitchen.insta_link = request.POST["insta_link"]
        if request.FILES:
            kitchen.kitchen_logo = request.FILES['kitchen_logo']
        kitchen.save()
        return HttpResponseRedirect(request.path_info)
    context = {
        "kitchen": kitchen
    }
    return render(request, "adminkitchen/adminkitchen.html", context)


@login_required(login_url="/login_adminkitchen")
def category_list(request):
    user = request.user
    kitchen = Kitchen.objects.get(user=user)
    categories = Category.objects.filter(kitchen=kitchen)
    context = {
        "kitchen": kitchen,
        "categories": categories
    }
    return render(request, 'adminkitchen/category_list.html', context)


@login_required(login_url="/login_adminkitchen")
def category_edit(request, pk):
    user = request.user
    kitchen = Kitchen.objects.get(user=user)
    category = Category.objects.get(id=pk)
    checked = ""

    if category.active == True:
        checked = "checked"   
    
    if request.method == "POST":
        category.category_title = request.POST["category_title"]
        category.active = request.POST.get('active', '') == 'on'
        category.save()
        return redirect(category_list)

    context = {
        "kitchen": kitchen,
        "category": category,
        "checked": checked
    }
    return render(request, "adminkitchen/category_edit.html", context)


@login_required(login_url="/login_adminkitchen")
def kitchen_location(request):
    user = request.user
    kitchen = Kitchen.objects.get(user=user)
    context = {
        "kitchen": kitchen
    }
    return render(request, "adminkitchen/kitchen_location.html", context)    
