from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from store.forms import CustomUserForm


def ragister(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Ragisterd Successfullu! Login To Continue.')
            return redirect('login/')
    context = {'form': form}
    return render(request, 'store/auth/ragister.html', context)


def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Your are already loged in')
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            passwd = request.POST.get('password')

            user = authenticate(request, username=name, password=passwd)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('/')
            else:
                messages.error(request, 'Invalid Username or Password')
                return redirect('loginpage')
    return render(request, 'store/auth/login.html')


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logout Successfully.')

    return redirect('/')
