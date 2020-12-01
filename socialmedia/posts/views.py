
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm, AddCommentForm
from .models import Post, Comment
from django.db import transaction
# from ..users.models import Profile
# @login_required
# def feed(request):
#     return render(request, 'feed/feed.html')
# new_author = f.save(commit=False)

# # Modify the author in some way.
# >>> new_author.some_field = 'some_value'

# # Save the new instance.
# >>> new_author.save()


@login_required
def feed(request):
    if request.method == 'POST':
        post_form = PostForm(
            request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request,
                             'Your profile was successfully updated!')
            return redirect(reverse('feed'))
        else:
            messages.error(request, 'Please correct the error below.')
    if request.method == "GET":
        post_form = PostForm()
        comment_form = AddCommentForm()
        users_to_include = [
            profile.user.id for profile in request.user.profile.friends.all()]
        users_to_include.append(request.user.id)
        feed = Post.objects.filter(
            user_id__in=users_to_include).order_by('-id')
        return render(request, 'feed/feed.html', {
            'post_form': post_form,
            'comment_form': comment_form,
            'posts': feed
        })


@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        comment_form = AddCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = Comment(
                user=request.user, comment=comment_form.data['q'])
            new_comment.save()
            post = Post.objects.get(pk=post_id)
            post.comments.add(new_comment)
            post.save()
            return redirect(reverse('feed'))
            

@login_required
@transaction.atomic
def edit_post(request, post_id):
    if request.method == 'POST':
        edit_form = PostForm( request.POST, instance=Post.objects.get(pk=post_id))
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request,
                             'Your post was successfully updated!')
            return redirect(reverse('feed'))
        else:
            messages.error(request, 'Please correct the error below.')
    if request.method == "GET":
        edit_form = PostForm(instance=Post.objects.get(pk=post_id))
        post_form = PostForm()
        comment_form = AddCommentForm()
        users_to_include = [
            profile.user.id for profile in request.user.profile.friends.all()]
        users_to_include.append(request.user.id)
        feed = Post.objects.filter(
            user_id__in=users_to_include).order_by('-id')
        return render(request, 'feed/feed.html', {
            'post_form': post_form,
            'edit_form': edit_form,
            'comment_form': comment_form,
            'posts': feed
        })