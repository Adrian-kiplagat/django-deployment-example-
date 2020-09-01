from django.shortcuts import render
from basic_app.forms import ProfileForm, UserForm
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def index(request):
    return render(request, 'basic_app/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def special(request):
    return HttpResponse('You are logged in nice!')


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(profile_form.errors, user_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, 'basic_app/registration.html', {'registered': registered, 'user_form': user_form, 'profile_form': profile_form})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account is not active')

        else:
            print('Someone tried to login and failed')
            print('Username:{} Password:{}'.format(username, password))
            return HttpResponse('Invalid login details')
    else:
        return render(request, 'basic_app/login.html', {})
