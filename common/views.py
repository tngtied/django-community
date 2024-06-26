from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from common.forms import UserForm, UserInfoForm
from pybo.models import Question, Category, Answer, Comment
from django.core.paginator import Paginator
from pybo.decorators import render_with_common
from django.contrib.auth.models import User

@render_with_common
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return {'context': {}, 'template': 'common/login.html'}
def logout_view(request):
    logout(request)
    return redirect('index')

# Create your views here.
@render_with_common
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    context = {'form': form}
    return {'context': context, 'template': 'common/signup.html'}
    # return render(request, 'common/signup.html', {'form': form})
@render_with_common
def category(request, category_id):
    posts = Question.objects.filter(category_id=category_id).order_by('-create_date')
    paginator = Paginator(posts, 10)
    page = paginator.get_page(1)
    category = Category.objects.get(pk=category_id)
    context = {'question_list':page, 'category':category, 'page':1}
    return {'context': context, 'template': 'pybo/question_list.html'}
    return render(request, 'pybo/question_list.html', context)

@render_with_common
def profile(request, user_id):
    if request.path == '/mypage/' and request.user.is_authenticated and request.user.id == user_id:
        user_id = request.user.id
    user = User.objects.get(pk=user_id)
    posts = Question.objects.filter(author=user).order_by('-create_date')
    paginator = Paginator(posts, 10)
    page = paginator.get_page(1)
    answers = Answer.objects.filter(author=user).order_by('-create_date')
    comments = Comment.objects.filter(author=user).order_by('-create_date')
    context = {'articles':page, 'page':1, 'user':user, 'answers':answers, 'comments':comments}
    return {'context': context, 'template': 'common/profile.html'}

@render_with_common
def profile_update(request):
    user = request.user
    if request.method == "POST":
        form = UserInfoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('common:mypage')
    else:
        form = UserInfoForm(instance=user)
    context = {'form': form}
    return {'context': context, 'template': 'common/user_info_change.html'}
    # return render(request, 'common/profile_update.html', context)
