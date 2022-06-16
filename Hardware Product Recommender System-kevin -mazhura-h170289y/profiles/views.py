from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, login_required, login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from pandas import Categorical

from shop.models import Product
from .forms import ProfForm, ProfileForm, CustomChangePasswordForm, ProfileIntrestsForm
from .models import *
from shop.models import *

def index(request):
    try:
        profile = Profile.objects.get(user=request.user.id)
        if profile:
            form = ProfForm(instance=profile)
        else:
            form = ProfForm()
    except ObjectDoesNotExist:
        profile = []
        current_user = User.objects.get(id=request.user.id)
        form = ProfForm()
    # Product.objects.order_by('-name')
    product_list = []
    user = User.objects.get(id=request.user.id)
    print(user)
    return render(request, 'profiles/new-profile.html', {'myprofile': profile,'user':user,'form':form,'product_list': product_list},)
    # return HttpResponse(product_list)

def profiles(request):
    """Load Homepage via Profile Link"""
    # form = ProfileForm(user=request.user)
    try:
        profile = get_object_or_404(Profile, user=request.user.id)
        if profile:
            form = ProfileForm(instance=profile)
        else:
            form = ProfileForm()
    except ObjectDoesNotExist:
        profiles = []
    product_list = Product.objects.order_by('-name')
    return render(request, 'profiles/index.html', {'myprofile': profile,'profile_form':form,'product_list': product_list},)
@login_required
def profile(request, profile_slug):
    """Load Profile"""
    print(profile_slug)
    profile = get_object_or_404(Profile, slug=profile_slug)
    categories = Category.objects.all()
    intrest_form = ProfileIntrestsForm
    my_intrests = ProfileIntrests.objects.filter(profile=profile)
    return render(request, 'profiles/profile.html', {'profile': profile,'my_intrests':my_intrests, 'categories':categories,'intrest_form':intrest_form})
@login_required
def add_intrest(request, profile_slug):
    """Load Profile"""
    print(profile_slug)
    if request.POST:
        interest = request.POST.get('intrest')
        print(interest)
        profile = get_object_or_404(Profile, slug=profile_slug)
        categories = Category.objects.all()
        intrest_form = ProfileIntrestsForm(data=request.POST)
        my_intrests = ProfileIntrests.objects.filter(intrest=interest)
        if len(my_intrests):
            print("allready exist!!")
        else:
            if intrest_form.is_valid:
                intrest_form.save()
                my_intrests = ProfileIntrests.objects.filter(profile=profile)
        
        return render(request, 'profiles/profile.html', {'profile': profile,'my_intrests':my_intrests, 'categories':categories,'intrest_form':intrest_form})


@login_required
def edit_profile(request, profile_slug):
    """Edit Profile Form"""
    profile = get_object_or_404(Profile, slug=profile_slug)
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "{} {}'s profile updated."
                             .format(form.cleaned_data["first_name"],
                                     form.cleaned_data["last_name"]))
            return HttpResponseRedirect(profile.get_absolute_url())
    return render(request, "profiles/edit-profile.html", {'form': form})


@login_required
def change_password(request, profile_slug):
    """Change Password Form"""
    if request.method == 'POST':
        form = CustomChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was '
                                      'successfully updated!')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomChangePasswordForm(request.user)
    return render(request, 'profiles/change-password.html', {
        'form': form
    })
