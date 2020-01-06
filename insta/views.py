from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Comment
from django.shortcuts import get_object_or_404
from .forms import UpdateProfileForm, UserUpdateForm, PostForm, CommentForm

# Create your views here.


def home(request):
    post = Post.objects.all()[::-1]

    return render(request, 'home.html', {"post": post})


@login_required(login_url='/accounts/login/')
def about(request):

    return render(request, 'test.html')


@login_required(login_url='/accounts/login')
def profile(request):
    title = "Profile"
    current_user = request.user
    posts = Post.get_user_posts(request.user.id)
    user_profile = Profile.objects.all()
    return render(request, 'profile.html', {"posts": posts , "user_profile":user_profile})


@login_required(login_url='accounts/login')
def update_profile(request):
	'''
    Function that renders the update profile template and passes the form into it.
    '''
	if request.method == 'POST':
		user_form = UserUpdateForm(request.POST ,instance=request.user )
		profile_form = UpdateProfileForm(request.POST,request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return redirect('Profile')
	else:
		user_form = UserUpdateForm(instance=request.user)
		profile_form = UpdateProfileForm()

	return render(request, 'updateprofile.html', {"user_form":user_form,"profile_form":profile_form})


@login_required(login_url='/accounts/login')
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = current_user
            post.save()
        return redirect('Home')
    else:
        form = PostForm()

    return render(request, 'new_post.html', {"form": form})


@login_required(login_url='/accounts/login')
def comment(request, id):
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.posted_by = request.user
            post = Post.objects.get(id=id)
            comment.post_id = post
            comment.save()
        return redirect('comment')
    else:
        form = CommentForm()

    image_posted = Post.single_image(id)
    image_id = Post.get_image_id(id)
    comments = Comment.get_post_comments(image_id)

    return render(request, 'comment.html', {"form": form, "comments": comments, "post": image_posted})
