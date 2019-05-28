from django.http import HttpResponseRedirect
from django.urls import reverse


def redirect_to_bethink(request):
    return HttpResponseRedirect(reverse('bethink:home'))
