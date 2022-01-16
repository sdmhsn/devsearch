from django.db.models import Q  # to using bitwise (&) and (|) operator to inside .filter() queryset API
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Profile, Skill


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_querykuuuuu'):  # search_querykuuuuu: is value from name attribute in profiles.html template
        search_query = request.GET.get('search_querykuuuuu')

    # print('SEARCH:', search_query)

    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.order_by('created').distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
    )  #  .filter(name__contains=search_query): matching operations. name: search by name, __icontains: matching by case insensitive (not case sensitive). distinct():  eliminates duplicate rows from the query results, we can also put the .distinct() after the .filter(). order_by('-created'): untuk sort dari terbaru ke yang terlama, ('created') untuk sort dari terlama ke yang terbaru, we can also handle this sorting by Meta class in users models.py
    # profiles = Profile.objects.all()
    # profiles = Profile.objects.filter()  # the functionality of empty parameter in filter(), will be similar to .all()

    return profiles, search_query


def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles, paginator
