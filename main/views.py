"""import django """
from django.shortcuts import render,redirect, get_object_or_404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import RegisterForm, PostForm
from .models import Post

@login_required(login_url="/login")
def home(request):
    """creating homepage content"""
    posts = Post.objects.all()

    if request.method == "POST":
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='agent')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass

    return render(request, 'main/home.html', {'posts': posts})

@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    """create post form redirection"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, 'main/create_post.html', {'form': form})

def sign_up(request):
    """ create user redirection and adding user to a group"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name=form.cleaned_data.get('group'))
            user.groups.add(group)
            user.group = form.cleaned_data.get('group')
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html',{'form': form})

@login_required(login_url="/login")
def post_single(request, post):
    """viewing single post content and checking if the
post is added to favourites"""
    post = get_object_or_404(Post,slug=post)
    fav = bool
    if post.favourites.filter(id=request.user.id).exists():
        fav = True
    return render(request, 'main/single.html', {'post': post,'fav':fav})

@login_required(login_url="/login")
def favourite_add(request, id):
    """add to favourite logic"""
    post = get_object_or_404(Post, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url="/login")
def favourite_list(request):
    """list all favourite posts logic"""
    posts = Post.objects.filter(favourites=request.user)
    return render(request,'main/favourites.html',{'posts':posts})
