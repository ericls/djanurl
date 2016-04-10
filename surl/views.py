from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from surl.models import Surl, Profile


def index_view(request):
    if request.user.is_authenticated():
        try:
            request.user.profile
        except Profile.DoesNotExist:
            Profile.objects.create(user=request.user)
    return render(request, 'surl/index.html', {})


def api_create_surl(request):
    url = request.POST.get('url')
    if not url:
        return JsonResponse({'error': 'empty URL'})
    if '.' not in url:
        return JsonResponse({'error': 'Invalid URL'})
    if '//' not in url:
        url = 'http://{}'.format(url)
    password = request.POST.get('password', '')
    surl = Surl.create_surl(url=url, user_id=request.user.pk, password=password)
    return JsonResponse({'surl': surl.slug})


def create_surl_view(request):  # If javascript is not enabled, fall back to this view
    if request.method == 'GET':
        return HttpResponse('Not Allowed', status=405)
    url = request.POST.get('url')
    password = request.POST.get('password', '')
    if not url:
        messages.add_message(request, messages.WARNING, 'URL不能为空')
        return HttpResponseRedirect(reverse('index'))
    if '.' not in url:
        messages.add_message(request, messages.WARNING, 'URL不合法')
        return HttpResponseRedirect(reverse('index'))
    if '//' not in url:
        url = 'http://{}'.format(url)
    surl = Surl.create_surl(url=url, user_id=request.user.pk, password=password)
    return render(request, 'surl/index.html', {'surl': surl})


def my_surl_view(request):
    if not request.user.is_authenticated():
        messages.add_message(request, messages.error, '请先登录')
        return HttpResponseRedirect(reverse('auth_login'))
    try:
        request.user.profile
    except Profile.DoesNotExist:
        Profile.objects.create(user=request.user)
    return render(request, 'surl/my.html', {'title': '我的短网址'})


def go_to_url(request, slug):
    explicit_redirect = getattr(settings, 'EXPLICIT_REDIRECT', False)
    if explicit_redirect:
        pass  # TODO: explicit redirection
    else:
        surl = Surl.objects.get(slug=slug)
        surl.increase_count()
        return HttpResponseRedirect(surl.url)
