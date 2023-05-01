from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles, paginateProfiles


# Create your views here.
def all_profile(request):
    all_user_profile, search_query = searchProfiles(request)
    custom_range, all_user_profile = paginateProfiles(request, all_user_profile, 6)

    context = {
        "all_user_profile": all_user_profile,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, 'users/all_user_profiles.html', context)


def user_profile(request, pk):
    user_profile = Profile.objects.get(id=pk)

    topSkill = user_profile.skill_set.exclude(description__exact="")
    otherSkill = user_profile.skill_set.filter(description="")

    context = {
        "user_profile": user_profile,
        "topSkill": topSkill,
        "otherSkill": otherSkill,
    }
    return render(request, 'users/user_profile.html', context)


def loginUserPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # try:
        #     user = User.objects.get(username=username)
        # except:
        #     messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or password is incorrect!')

    return render(request, 'users/login_register.html')


def logoutUserPage(request):
    logout(request)
    messages.info(request, 'User successfully logged out!')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user.username = user.username.lower()
            # user.save()

            messages.success(request, "Your Account was created successfully!")
            login(request, user)
            return redirect('edit_account')
        else:
            messages.error(request, "User Account not created")

    context = {"page": page, "form": form}
    return render(request, 'users/login_register.html', context=context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
    }
    return render(request, 'users/my_account.html', context=context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {
        "form": form,
    }
    return render(request, 'users/account_form.html', context=context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')

    context = {
        "form": form,
    }
    return render(request, 'users/skill_form.html', context=context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill successfully updated")
            return redirect('account')

    context = {
        "form": form,
    }
    return render(request, 'users/skill_form.html', context=context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill successfully deleted")
        return redirect('account')

    context = {
        "object": skill,
    }
    return render(request, 'MyProject/delete_object.html', context=context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unread_count = messageRequests.filter(is_read=False).count()

    context = {
        "messageRequests": messageRequests,
        "unread_count": unread_count,
    }
    return render(request, 'users/inbox.html', context=context)


@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if not message.is_read:
        message.is_read = True
        message.save()
    context = {
        "message": message,
    }
    return render(request, 'users/message.html', context=context)


# @login_required(login_url='login')
def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "Your message was successfully sent!")
            return redirect('user_profile', pk=recipient.id)

    context = {
        "recipient": recipient,
        "form": form,
    }
    return render(request, 'users/message_form.html', context=context)
