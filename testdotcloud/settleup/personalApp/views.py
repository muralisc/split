# Django imports
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
# app imports
from personalApp.models import Transfers


def from_category_view(request):
    return render_to_response('personalTemplates/fromSelect.html', locals(), context_instance=RequestContext(request))


def to_category_view(request):
    return render_to_response('personalTemplates/toSelect.html', locals(), context_instance=RequestContext(request))


def amount_view(request):
    return render_to_response('personalTemplates/amountSelect.html', locals(), context_instance=RequestContext(request))


def description_view(request):
    return render_to_response('personalTemplates/descriptionSelect.html', locals(), context_instance=RequestContext(request))


def time_view(request):
    return render_to_response('personalTemplates/timeSelect.html', locals(), context_instance=RequestContext(request))
