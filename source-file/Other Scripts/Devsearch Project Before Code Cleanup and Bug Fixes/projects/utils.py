from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project


def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__name__icontains=search_query)
    ) # we can also put the .distinct() after the .filter()

    return projects, search_query


def paginateProjects(request, projects, results):
    page = request.GET.get('page')  # to get value on 'page' keyword on url browser. the 'page' will take in attribute href (href="?page={{ page }}" ) inside pagination tags in the projects.html template
    # results = 3  # how many items / results of project will show per page (in this case is 3 results of projects per page). in this example results move to the paginateProjects() parameter
    paginator = Paginator(projects, results)  # the Paginator class. list of objects
    # print(paginator.count)  # to get how many project that we have

    try:
        projects = paginator.page(page)  # paginator.page(page): to getting / entering the page by the 'page' variable. for example when we enter to http://127.0.0.1:8000/projects/?page=1 will show page 1 of 3
    except PageNotAnInteger:  # PageNotAnInteger: when we don't have any page search parameters. for example when we enter to http://127.0.0.1:8000/projects/ not http://127.0.0.1:8000/projects/?page=1
        page = 1
        projects = paginator.page(page)  # we will redirect to page 1
    except EmptyPage:  # EmptyPage: that page contains no results. for example when we enter to http://127.0.0.1:8000/projects/?page=10000000000000000000
        page = paginator.num_pages  # .num_pages:  the total number of pages. to return / show how many pages will create, by devide between projects (queryset) and results in Paginator
        projects = paginator.page(page)  # will redirect to the last page (the total number)

    # extra logics to handle total output (custom range) of pagination button in a page. so if we have thousand pages, we will not see all of those buttons:
    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    '''
    example:
    page = 6 # to page no 6
    leftIndex = 6 - 4 = 2 # 2 < 1 = false, so the value is 2

    rightIndex = 6 + 5 = 11 # 11 > paginator.num_pages (we have 6 pages) = true, so the value is 7

    custom_range = range(2, 7) # this will show up pagination button 2 until 6
    '''

    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects, paginator  # we still return paginator for last button functionality
