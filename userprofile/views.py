from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from .models import Profile


def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return redirect("article:article_list")
            else:
                return HttpResponse('账号或密码有误')
        else:
            return HttpResponse('输入不合法')

    elif request.method == "GET":
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse('请求方式有误')


def user_logout(request):
    logout(request)
    return redirect("article:article_list")


def user_register(request):
    if request.method == "POST":
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse('表单填写有误')
    else:
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)


@login_required(login_url='userprofile/login')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user_id=id)

    if request.method == "POST":
        if request.user != user:
            return HttpResponse('无修改权限')

        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():

            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            print('true')
            print(request)
            print(request.FILES)

            if 'avatar' in request.FILES:
                print('true')
                profile.avatar = profile_cd['avatar']

            profile.save()
            return redirect('userprofile:edit', id=id)
        else:
            return HttpResponse('invalid input')
    elif request.method == "GET":
        profile_form = ProfileForm()
        context = {
            'profile_form': profile_form,
            "profile": profile,
            "user": user
        }
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse('invalid request~')
