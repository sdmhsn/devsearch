from django.contrib.auth import login
from django.core import paginator
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError
from .models import Project
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects


def projects(request):
    projects, search_query = searchProjects(request)  # projects: querysets API data .filter() similar with .all() when we didn't match any keyword into the search input yet
    custom_range, projects, paginator = paginateProjects(request, projects, 6)

    context = {
        'projects': projects,
        'search': search_query,
        'paginator': paginator,
        'custom_range': custom_range,
    }

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)        
        try:
            review = form.save(commit=False)
            review.owner = request.user.profile  # if the request.user.profile is outside on if statement (example: profile = request.user.profile), anonymous user (user didn't login yet) can't access / view the project when we opened it (error)
            review.project = projectObj
            review.save()
            projectObj.getVoteCount
            messages.success(request, 'Your review was successfully submitted!')
            return redirect('project', pk=projectObj.id)
        except IntegrityError:
            messages.error(request, 'You already post review!')
            return redirect('project', pk=projectObj.id)
        except AttributeError:
            messages.error(request, 'You have to login before leave review!')
            return redirect('project', pk=projectObj.id)
        
    context = {'project': projectObj, 'form': form}

    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile  # to ensure that only a logged in user and the owner of a particular project can create it
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid:
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, 'Project was added successfully!')
            return redirect('account')

    context = {'form': form}
    # print(form)

    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk) # to ensure that only a logged in user and the owner of a particular project can edit / update it. project_set: query models children
    form = ProjectForm(instance=project)
    # print(form)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid:
            form.save()
            messages.success(request, 'Project was added updated!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)  # to ensure that only a logged in user and the owner of a particular project can delete it. project_set: query models children

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project was deleted successfully!')
        return redirect('account')

    context = {'object': project}
    return render(request, 'delete-template.html', context)
