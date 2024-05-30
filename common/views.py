from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from common.forms import UserForm
from pybo.models import Question, Category
from django.core.paginator import Paginator
from pybo.views.common_render import render_with_common

def logout_view(request):
    logout(request)
    return redirect('index')

# Create your views here.
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
    return render(request, 'common/signup.html', {'form': form})
@render_with_common
def category(request, category_id):
    posts = Question.objects.filter(category_id=category_id).order_by('-create_date')
    paginator = Paginator(posts, 10)
    page = paginator.get_page(1)
    category = Category.objects.get(pk=category_id)
    context = {'question_list':page, 'category':category, 'page':1}
    return {'context': context, 'template': 'pybo/question_list.html'}
    return render(request, 'pybo/question_list.html', context)