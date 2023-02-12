"""import django methods for redirecting user and
checking if the user is logged or has permision
and importing the models from database and forms
to create the elements in the database"""
from django.shortcuts import render,redirect, get_object_or_404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import RegisterForm, PostForm, ReviewForm, InspectionForm
from .models import Post, ReviewRating,Inspection,ConversationMessage,Notification
from .models import User
#from .utilities import create_notification
#from .context_processors import notifications


@login_required(login_url="/login")
def home(request):
    """creating homepage content logic"""
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
    """create posts logic"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/home')
    else:
        form = PostForm()

    return render(request, 'main/create_post.html', {'form': form})

def sign_up(request):
    """create user and adding user to a group"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name=form.cleaned_data.get('group'))
            user.groups.add(group)
            user.group = form.cleaned_data.get('group')
            user.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html',{'form': form})

@login_required(login_url="/login")
def post_single(request, post_id):
    """viewing single post content and checking if the
post is added to favourites and calculating rating"""
    post = get_object_or_404(Post,id=post_id)
    fav = bool
    if post.favourites.filter(id=request.user.id).exists():
        fav = True
    ratings = ReviewRating.objects.filter(post=post)
    rating_count = ReviewRating.objects.filter(post=post).count()
    rating = -1
    if rating_count != 0:
        rating_sum = 0
        for rating in ratings:
            rating_sum += rating.rating
        rating = rating_sum/rating_count
    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            #conversationmessage = ConversationMessage.objects.create(
                                                                    #post=post,content=content, created_by=request.user)

            #create_notification(request, post.author, 'message', extra_id=post.id)

            return redirect('post_single', post_id=post_id)
    return render(request, 'main/post_single.html', {'post': post,'fav':fav,'rating':rating})

@login_required(login_url="/login")
def dashboard(request):
    """ lists created posts for agents or lists
    asked for inspection forms for buyers logic"""
    posts = Post.objects.filter(author=request.user)
    return render(request, 'main/dashboard.html',
                {'userprofile':request.user.userprofile,'posts':posts})

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

@login_required(login_url="/login")
def submit_review(request, post):
    """submit review logic"""
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user=request.user, post=post)
            form = ReviewForm(request.POST,instance=reviews)
            form.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = ReviewRating()
                review.rating = form.cleaned_data['rating']
                review.internet_protocol= request.META.get('REMOTE_ADDR')
                review.user_id = request.user.id
                review.post_id = post
                review.save()
                return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url="/login")
def inspect(request, post_id):
    """ask for inspection logic"""
    post = Post.objects.get(id=post_id)
    form = InspectionForm(request.POST)

    if request.method == 'POST':
        form = InspectionForm(request.POST)

        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.post = post
            inspection.created_by = request.user
            inspection.save()
            #create_notification(request, post.author, 'inspection', extra_id=post.id)
            return redirect('dashboard')

        form = InspectionForm()
    return render(request, 'main/inspection.html', {'form': form})

@login_required(login_url="/login")
def view_inspection(request, inspection_id):
    """view single inspection logic"""
    inspection = get_object_or_404(Inspection, id=inspection_id, created_by=request.user)
    return render(request,'main/view_inspection.html', {'inspection':inspection})

@login_required(login_url="/login")
def notifications(request):
    """making notification logic and going to the inspection created for post"""
    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)
    extra_id = request.GET.get('extra_id', 0)

    if goto != '':
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()

        if notification.notification_type == Notification.MESSAGE:
            return redirect('view_inspection', inspection_id=notification.extra_id)
        if notification.notification_type == Notification.INSPECTION:
            return redirect('view_inspection', inspection_id=notification.extra_id)

    return render(request, 'main/notifications.html')
