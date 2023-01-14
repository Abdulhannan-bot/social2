from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
# Create your views here.

from .models import *
from .forms import *
from .decorators import *

@unauthenticated_user
def register_view(request):
  form = SignUpForm()
  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
      try:
        form.save()
        messages.info(request,'Account created successfully')
        return redirect("login")
      except ValueError:
        messages.error(request,'Account with that username already exists. Pick another username')
  context = {
    "form": form,
  }
  return render(request, "register.html", context)

@unauthenticated_user
def login_view(request):
  if(request.method == "POST"):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    user1 = User.objects.filter(username = username).filter(password = password)
    print(user1)
    if(user is not None):
      login(request, user)
      return redirect('home')
    else:
      print("not authenticated")
  return render(request, "login.html")

@login_required(login_url = 'login')
def home(request):
  follows = Follower.objects.all()
  exclude_list = [request.user]
  account = Account.objects.get(user = request.user)
  account_list = [account]
  for i in follows:
    if(str(i.follower_id) == str(request.user.username)):
      user_instance = User.objects.get(username = str(i.followee_id))
      account_instance = Account.objects.get(user = user_instance)
      exclude_list.append(user_instance)
      account_list.append(account_instance)
  accounts = Account.objects.exclude(user__in = exclude_list)
  account_search = accounts
  value =""

  PostFormset = inlineformset_factory(Account, Post, fields=('post',), extra=1)
  account = Account.objects.get(user = request.user)
  formset = PostFormset(queryset = Post.objects.none(), instance = account)

  if request.method == "POST":
    if request.POST.get('searched'):
      print(request.POST)
      search = request.POST.get('searched',False)
      value = search
      account_search = Account.objects.filter(user__username__icontains=search)
    

  count = Account.objects.all().count() - accounts.count() - 1
  posts = ""
  following = ""
  likes = ""
  likes_list = []
  if count:
    posts = reversed(Post.objects.filter(user_id__in = account_list).order_by('created_at'))
    following = Follower.objects.filter(follower_id = account)
    likes = Like.objects.filter(liked_by = request.user.account)
    for i in likes:
      likes_list.append(i.post_id.post)
  comments_form = CommentForm()
  
  context = {
    "accounts": accounts,
    "count": count,
    "following": following,
    "likes": likes,
    "likes_list": likes_list,
    "posts": posts,
    "account_search": account_search,
    "value": value,
    "formset": formset,
    "comments_form": comments_form,
  }
  return render(request, "home.html", context = context)

@login_required(login_url = 'login')
def add_followee(request, id):
  print("followee entered")
  follower = Account.objects.get(user = request.user)
  followee = Account.objects.get(id = id)
  Follower.objects.create(follower_id = follower, followee_id = followee)

  return redirect('home')

@login_required(login_url = 'login')
def follower_profile(request, id):
  print("entered")
  account = Account.objects.get(id = id)
  posts = Post.objects.filter(user_id = account)
  followers = Follower.objects.filter(followee_id = account).count()
  following = Follower.objects.filter(follower_id = account).count()
  like = Like.objects.filter(user_id = account).count()
  follow = False
  post_show = False
  posts = Post.objects.filter(user_id = account)
  post_count = 0
  for post in posts:
    post_count += post.like_set.count()
  print(post_count)
  
  if Follower.objects.filter(follower_id = request.user.account).filter(followee_id = account).exists():
    follow = True
    post_show = True

  context = {
    "account": account,
    "posts": posts,
    "followers": followers,
    "following": following,
    "follow": follow,
    "posts": posts,
    "post_show": post_show,
    "like": like,
  }
  return render(request, "follower-profile.html", context = context)

@login_required(login_url = 'login')
def remove_followee(request, id):
  account = Account.objects.get(user = request.user)
  following = Follower.objects.filter(follower_id = account).filter(followee_id = Account.objects.get(id = id))
  following.delete()
  context = {
    "following":following,
  }
  return redirect('home')

@login_required(login_url = 'login')
def settings(request):
  account = Account.objects.get(user = request.user)
  user = User.objects.get(username = request.user.username)
  posts = Post.objects.filter(user_id = account)
  form = AccountForm(instance = account)
  if request.method == 'POST':
    form = AccountForm(request.POST, request.FILES, instance = account)
    if form.is_valid():
      form.save()
  context = {
    "form": form,
    "account": account,
    "posts": posts,
  }
  return render(request, "your-profile.html", context = context)

@login_required(login_url = 'login')    
def likes(request, id):
  post = Post.objects.get(id = id)
  user = User.objects.get(username = post.user_id)
  account = Account.objects.get(user = user)
  like_by = Account.objects.get(user = request.user)
  Like.objects.create(user_id = account, post_id = post, liked_by = like_by)
  context = {
    "liked": True,
  }
  return redirect('home')

@login_required(login_url = 'login')
def unlike(request, id):
  post = Post.objects.get(id = id)
  user = User.objects.get(username = post.user_id)
  account = Account.objects.get(user = user)
  like = Like.objects.filter(post_id = post).filter(user_id = account).filter(liked_by = request.user.account)
  like.delete()
  context = {
    "liked": False,
  }
  return redirect('home')

@login_required(login_url = 'login')
def add_post(request):
  PostFormset = inlineformset_factory(Account, Post, fields=('post',), extra=1)
  account = Account.objects.get(user = request.user)
  formset = PostFormset(queryset = Post.objects.none(), instance = account)
  if request.method == 'POST':
    formset = PostFormset(request.POST, request.FILES, instance = account)
    if formset.is_valid():
      formset.save()
  return redirect('home')
  # context = {
  #   "formset": formset,
  # }
  # return render(request, "add-post.html", context)

@login_required(login_url = 'login')
def add_comment(request, id):
  post = Post.objects.get(id = id)
  form = CommentForm()
  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      obj = form.save(commit = False)
      obj.post_id = post
      obj.user_id = request.user.account
      obj.save()
  return redirect('home')
  # context = {
  #   "form": form,
  # }
  # return render(request, "add-comment.html", context = context)

@login_required(login_url = 'login')
def delete_post(request, id):
  post = Post.objects.get(id = id)
  post.delete()
  return redirect('settings')


@login_required(login_url = 'login')
def logout_trigger(request):
  logout(request)
  return redirect('login')