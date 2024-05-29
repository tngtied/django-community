from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from common.forms import UserForm

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
def category(request):
    return render(request, 'common/category.html')