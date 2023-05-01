from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    search_skill = Skill.objects.filter(name__icontains=search_query)

    all_user_profile = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=search_skill)
    )

    return all_user_profile, search_query


def paginateProfiles(request, all_user_profile, results):
    page = request.GET.get('page')
    paginator = Paginator(all_user_profile, results)

    try:
        all_user_profile = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        all_user_profile = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        all_user_profile = paginator.page(page)

    leftIndex = int(page) - 4
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, all_user_profile