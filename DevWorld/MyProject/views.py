from django.shortcuts import render, redirect
from .models import Project
from .forms import MyProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProject, paginateProject
from django.contrib import messages


# Create your views here.
def projects(request):
    myproject, search_query = searchProject(request)
    custom_range, myproject = paginateProject(request, myproject, 6)

    context = {
        "myproject": myproject,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, 'MyProject/HomePage.html', context=context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        projectObj.getVoteCount

        messages.success(request, "Your Review was successfully submitted")
        return redirect('project', pk=projectObj.id)

    context = {
        "projectObj": projectObj,
        "form": form,
    }
    return render(request, 'MyProject/singleProject.html', context)


@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = MyProjectForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = profile
        project.save()
        return redirect('account')
    context = {
        "form": form,
    }
    return render(request, 'MyProject/project_form.html', context)


@login_required(login_url="login")
def update_project(request, pk):
    profile = request.user.profile
    update_object = profile.project_set.get(id=pk)
    form = MyProjectForm(instance=update_object)

    if request.method == 'POST':
        form = MyProjectForm(request.POST, request.FILES or None, instance=update_object)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {
        "form": form,
    }
    return render(request, 'MyProject/project_form.html', context)


@login_required(login_url="login")
def delete_project(request, pk):
    profile = request.user.profile
    delete_object = profile.project_set.get(id=pk)
    if request.method == 'POST':
        delete_object.delete()
        return redirect('account')
    context = {
        "object": delete_object,
    }
    return render(request, 'MyProject/delete_object.html', context)

