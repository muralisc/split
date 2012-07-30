# Django imports
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
# app imports
from personalApp.models import Transfers
from personalApp.forms import transferForm
# Python imports
import datetime


def from_category_view(request):
    form = transferForm()
    if request.method == "POST":
        form = transferForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['fromCategory'] != '':
                currentTransfer = Transfers()
                currentTransfer.fromCategory = form.cleaned_data['fromCategory']
                request.session['currentTransfer'] = currentTransfer
                return redirect('/personalApp/toCategory/')
            else:
                errors = "enter some category"
    return render_to_response('personalTemplates/fromSelect.html', locals(), context_instance=RequestContext(request))


def to_category_view(request):
    if 'currentTransfer' not in request.session:
        return redirect('/personalApp/fromCategory/')
    else:
        form = transferForm()
        if request.method == "POST":
            form = transferForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['toCategory'] != '':
                    request.session['currentTransfer'].toCategory = form.cleaned_data['toCategory']
                    request.session.modified = True
                    return redirect('/personalApp/amount/')
                else:
                    errors = "enter some category"
    return render_to_response('personalTemplates/toSelect.html', locals(), context_instance=RequestContext(request))


def amount_view(request):
    if 'currentTransfer' not in request.session:
        return redirect('/personalApp/fromCategory/')
    else:
        form = transferForm()
        if request.method == "POST":
            form = transferForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['amount'] != None:
                    if "finish" in request.POST:
                        request.session['currentTransfer'].amount = form.cleaned_data['amount']
                        request.session['currentTransfer'].description = ""
                        request.session['currentTransfer'].timestamp = datetime.datetime.now()
                        request.session.modified = True
                        return redirect('/personalApp/summary/')
                    #elif "nextPage" in request.POST:
                    else:
                        request.session['currentTransfer'].amount = form.cleaned_data['amount']
                        request.session.modified = True
                        return redirect('/personalApp/description/')
                else:
                    errors = "enter some money"
    return render_to_response('personalTemplates/amountSelect.html', locals(), context_instance=RequestContext(request))


def description_view(request):
    if 'currentTransfer' not in request.session:
        return redirect('/personalApp/fromCategory/')
    else:
        form = transferForm()
        if request.method == "POST":
            form = transferForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['description'] != None:
                    if "finish" in request.POST:
                        request.session['currentTransfer'].description = form.cleaned_data['description']
                        request.session['currentTransfer'].timestamp = datetime.datetime.now()
                        request.session.modified = True
                        return redirect('/personalApp/summary/')
                    #elif "nextPage" in request.POST:
                    else:
                        request.session['currentTransfer'].description = form.cleaned_data['description']
                        request.session.modified = True
                        return redirect('/personalApp/time/')
                else:
                    errors = "enter some description"
    return render_to_response('personalTemplates/descriptionSelect.html', locals(), context_instance=RequestContext(request))


def time_view(request):
    if 'currentTransfer' not in request.session:
        return redirect('/personalApp/fromCategory/')
    else:
        form = transferForm()
        if request.method == "POST":
            form = transferForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['timestamp'] != None:
                    if "finish" in request.POST:
                        request.session['currentTransfer'].timestamp = form.cleaned_data['timestamp']
                        request.session.modified = True
                        return redirect('/personalApp/summary/')
                    #elif "nextPage" in request.POST:
                    else:
                        request.session['currentTransfer'].timestamp = form.cleaned_data['timestamp']
                        request.session.modified = True
                        return redirect('/personalApp/summary/')
                else:
                    errors = "enter some time"
    return render_to_response('personalTemplates/timeSelect.html', locals(), context_instance=RequestContext(request))


def summary(request):
    if 'currentTransfer' not in request.session:
        return redirect('/personalApp/fromCategory/')
    else:
        currentTransfer = request.session['currentTransfer']
        if request.method == "POST":
            currentTransfer.save()
            request.session.flush()
            return redirect('/personalApp/fromCategory/')
    return render_to_response('personalTemplates/summary.html', locals(), context_instance=RequestContext(request))
