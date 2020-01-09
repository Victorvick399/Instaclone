from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Comment
from django.shortcuts import get_object_or_404
from .forms import ProfileForm, UpdateUserForm, PostForm, CommentForm

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
    
    return render(request, 'profile.html', {"posts": posts })


@login_required(login_url='accounts/login')
def update_profile(request):
	'''
    Function that renders the update profile template and passes the form into it.
    '''
	current_user = request.user
	if request.method == 'POST':
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		if profile_form.is_valid():
			Profile.objects.filter(user_id=current_user.id).delete()
			profile = profile_form.save(commit=False)
			profile.user = current_user
			profile.save()
			return redirect("Profile")
	else:
		profile_form = ProfileForm()

	return render(request, 'updateprofile.html', {"profile_form":profile_form})


@login_required(login_url='/accounts/login')
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)
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

def search_results(request):
    if 'user' in request.GET and request.GET["user"]:

        search_term=request.GET.get('user')
        try:
            posts_name=Post.get_posts(search_term)
            message=f'{search_term}'
            title="Searched"

            if posts_name:  
                return render(request, 'search.html',{"posts":posts_name,"title":title,"message":message})
        except ObjectDoesNotExist:        
            message=f'{search_term}'
            title="Searched"
            return render(request, 'search.html',{"title":title,"message":message})

        try:
            user_found=User.objects.get(username=search_term)      
            user_posts=Post.get_user_posts(user_found.id)
            message=f'{search_term}'
            title="Searched"
            if user_posts or follow_user:                                        
                return render(request, 'search.html',{"user_f":user_found,"posts":user_posts,"title":title,"message":message})
        except ObjectDoesNotExist:
            message=f'{search_term}'
            title="Searched"
            return render(request, 'search.html',{"title":title,"message":message})   