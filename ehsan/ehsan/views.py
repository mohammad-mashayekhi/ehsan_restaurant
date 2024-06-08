from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next', 'dashboard')  # پیش‌فرض 'dashboard'
                return redirect(next_url)  # به صفحه اصلی یا صفحه دلخواه خودتان ریدایرکت کنید
            else:
                form.add_error(None, 'نام کاربری یا رمز عبور اشتباه است.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'main/login.html', {'form': form, 'next': request.GET.get('next', '')})