
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
# from users.forms import CustomUserCreationForm
from users.forms import ProfileForm, UserForm, CustomUserCreationForm, SearchProfileForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Profile


def dashboard(request):
    return render(request, 'users/dashboard.html')


def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,
                             'Your profile was successfully updated!')
            return redirect(reverse('dashboard'))
        else:
            messages.error(request, 'Please correct the error below.')
    if request.method == "GET":
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'users/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })


@login_required
def find_profile(request):
    if request.method == 'POST':
        find_form = SearchProfileForm(request.POST)
        if find_form.is_valid():
            users_to_exclude = [
                profile.user.id for profile in request.user.profile.friends.all()]
            users_to_exclude.append(request.user.id)
            result = Profile.objects.filter(
                user__username__contains=find_form.data['q']).exclude(user_id__in=users_to_exclude)
            return render(request, 'users/friends.html', {
                'find_form': find_form,
                'profiles': result
            })
        else:
            messages.error(request, 'Please correct the error below.')
    if request.method == "GET":
        find_form = SearchProfileForm()
        users_to_exclude = [
            profile.user.id for profile in request.user.profile.friends.all()]
        users_to_exclude.append(request.user.id)
        last_ten = Profile.objects.all().exclude(
            user_id__in=users_to_exclude).order_by('-id')[:10]
        return render(request, 'users/friends.html', {
            'find_form': find_form,
            'profiles': last_ten
        })


@login_required
def follow_profile(request, profile_id):
    current_profile = Profile.objects.get(pk=request.user.profile.id)
    follow_profile = Profile.objects.get(pk=profile_id)
    current_profile.friends.add(follow_profile)
    follow_profile.friends.add( current_profile)
    follow_profile.save()
    current_profile.save()
    return redirect(reverse('dashboard'))


@login_required
def my_following_followers(request):
    user_profile = Profile.objects.get(user_id=request.user.id)
    friends = user_profile.friends.all()
    return render(request, 'users/friends_overview.html', {
        'friends': friends
    })
