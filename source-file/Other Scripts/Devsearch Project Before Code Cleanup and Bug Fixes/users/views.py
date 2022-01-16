from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm  # change to CustomUserCreationForm in forms.py
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User  # related to User in admin
from .models import Profile
from .forms import ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles


def profiles(request):
    ''' 
        # This search scripts move to utils.py
        search_query = ''

        if request.GET.get('search_querykuuuuu'):  # search_querykuuuuu: is value from name attribute in profiles.html template
            search_query = request.GET.get('search_querykuuuuu')

        # print('SEARCH:', search_query)
        
        skills = Skill.objects.filter(name__icontains=search_query)

        profiles = Profile.objects.distinct().filter(
            Q(name__icontains=search_query) |
            Q(short_intro__icontains=search_query) |
            Q(skill__in=skills)
        )  #  .filter(name__contains=search_query): matching operations. name: search by name, __icontains: matching by case insensitive (not case sensitive). distinct():  eliminates duplicate rows from the query results, we can also put the .distinct() after the .filter()
        # profiles = Profile.objects.all()
        # profiles = Profile.objects.filter()  # the functionality of empty parameter in filter(), will be similar to .all()
    '''
    
    profiles, search_query = searchProfiles(request)
    custom_range, profiles, paginator = paginateProfiles(request, profiles, 2)
    
    context = {
        'profiles': profiles,
        'search': search_query,
        'custom_range': custom_range,
        'paginator': paginator
    }
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact='')
    otherSkills = profile.skill_set.filter(description='')

    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        # print(request.POST)
        username = request.POST['username'].lower()  # .lower(): to ensure that everything we input into the username input form, will always be lowercase (no case sensitivity)
        password = request.POST['password']
        # print(password)

        # try: # PR!!!!!
            # user = User.objects.get(username=username)
        # except:
            # messages.error(request, 'Username does not exist!') # alert color: red

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, 'User was logged in!')
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')  # if there is 'next' in request.GET (login through by project), execute login by request.GET['next'], if not (through by login) execute by account
        else:  # this cause the close button (x) can't close the alert
            messages.error(request, 'Username OR Password is incorrect!')  # alert color: red

    return render(request, 'users/login-register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!') # alert color: blue
    return redirect('login')


def registerUser(request):
    if request.user.is_authenticated:  # tambahan
        return redirect('profiles')
    
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            messages.success(request, 'User account was created!')  # alert color: green
            user.save()
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'users/login-register.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()
            messages.info(request, 'Profile was updated!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile-form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid:
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk) # skill_set: query models children
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid:
            form.save()
            messages.success(request, 'Skill was added updated!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)  # skill_set: query models children

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')
    
    context = {'object': skill}
    return render(request, 'delete-template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    if message.is_read == False:
        message.is_read = True
        message.save()
        
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
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
            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'form': form, 'recipient': recipient}
    return render(request, 'users/message_form.html', context)
