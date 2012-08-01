# Django imports
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.db.models import Count, Sum
from django.db.models import Q
# app imports
from personalApp.models import Transfers
from personalApp.forms import transferForm, filterForm
# Python imports
import datetime
import itertools
# TODO user support for pf


def from_category_view(request):
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
    else:
        form = transferForm()
        fromDistinct = Transfers.objects.values(
                                    'fromCategory'
                                    ).annotate(
                                    no_of_occ=Count('fromCategory')
                                    ).order_by(
                                    '-no_of_occ'
                                    )
        toDistinct = Transfers.objects.filter(
                                    #exclude alredy selected Category values
                                    ~Q(toCategory__in=[i['fromCategory'] for i in fromDistinct])
                                    ).values(
                                    'toCategory'
                                    ).annotate(
                                    no_of_occ=Count('toCategory')
                                    ).order_by(
                                    '-no_of_occ'
                                    )
        optionList = list()
        for i in fromDistinct:
            optionList.append(i['fromCategory'])
        for i in toDistinct:
            optionList.append(i['toCategory'])
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
                    currentTransfer = request.session['currentTransfer']
                    currentTransfer.toCategory = form.cleaned_data['toCategory']
                    request.session['currentTransfer'] = currentTransfer
                    return redirect('/personalApp/amount/')
                else:
                    errors = "enter some category"
        else:
            currentTransfer = request.session['currentTransfer']
            possibleToDistinct = Transfers.objects.filter(
                                                Q(fromCategory=currentTransfer.fromCategory)
                                                ).values(
                                                'toCategory'
                                                ).annotate(
                                                no_of_occ=Count('toCategory')
                                                ).order_by(
                                                '-no_of_occ'
                                                )
            toDistinct = Transfers.objects.filter(
                                                #exclude alredy selected Category values
                                                ~Q(toCategory__in=[i['toCategory'] for i in possibleToDistinct])
                                                ).values(
                                                'toCategory'
                                                ).annotate(
                                                no_of_occ=Count('toCategory')
                                                ).order_by(
                                                '-no_of_occ'
                                                )
            fromDistinct = Transfers.objects.filter(
                                                #exclude alredy selected Category values
                                                ~Q(fromCategory__in=[i['toCategory'] for i in possibleToDistinct]),
                                                ~Q(fromCategory__in=[i['toCategory'] for i in toDistinct])
                                                ).values(
                                                'fromCategory'
                                                ).annotate(
                                                no_of_occ=Count('fromCategory')
                                                ).order_by(
                                                '-no_of_occ'
                                                )
        optionList = list()
        for i in possibleToDistinct:
            optionList.append(i['toCategory'])
        for i in toDistinct:
            optionList.append(i['toCategory'])
        for i in fromDistinct:
            optionList.append(i['fromCategory'])
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
                    currentTransfer = request.session['currentTransfer']
        else:
            currentTransfer = request.session['currentTransfer']
            possibleAmountDistinct = Transfers.objects.filter(
                                                Q(fromCategory=currentTransfer.fromCategory),
                                                Q(toCategory=currentTransfer.toCategory)
                                                ).values(
                                                'amount'
                                                ).annotate(
                                                no_of_occ=Count('amount')
                                                ).order_by(
                                                '-no_of_occ'
                                                )
            optionList = list()
            for i in possibleAmountDistinct:
                optionList.append(i['amount'])
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
                # i.e user pressed finish without entering anything
                elif "finish" in request.POST:  # (implied)and form.cleaned_data['description'] == None
                    request.session['currentTransfer'].timestamp = datetime.datetime.now()
                    request.session.modified = True
                    return redirect('/personalApp/summary/')
                else:
                    errors = "enter some description"
        else:
            currentTransfer = request.session['currentTransfer']
            possibleDescDistinct = Transfers.objects.filter(
                                                Q(fromCategory=currentTransfer.fromCategory),
                                                Q(toCategory=currentTransfer.toCategory)
                                                ).values(
                                                'description'
                                                ).annotate(
                                                no_of_occ=Count('description')
                                                ).order_by(
                                                '-no_of_occ'
                                                )
            descDistinct = Transfers.objects.filter(
                                                #exclude alredy selected Category values
                                                ~Q(description__in=[i['description'] for i in possibleDescDistinct])
                                                ).values(
                                                'description'
                                                ).annotate(
                                                no_of_occ=Count('description')
                                                ).order_by(
                                                '-no_of_occ'
                                                )
            optionList = list()
            for i in possibleDescDistinct:
                optionList.append(i['description'])
            for i in descDistinct:
                optionList.append(i['description'])
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
                elif "finish" in request.POST:  # (implied)and form.cleaned_data['description'] == None
                    request.session['currentTransfer'].timestamp = datetime.datetime.now()
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
        # if request.method == "POST":
        currentTransfer.save()
        request.session.flush()
        return redirect('/personalApp/fromCategory/')
    # this is stll here beacuse --> just in case
    return render_to_response('personalTemplates/summary.html', locals(), context_instance=RequestContext(request))


def statistics(request):
    transferFilters = Q()
    if request.method == "POST":
        # form = filterForm(transferList, request.POST)
        if 'delete' in request.POST:
            xferIdToDelete = request.POST['delete']
            Transfers.objects.get(pk=xferIdToDelete).delete()
        # filter the data based in the filters
        if request.POST['fromCategory'] != '':
            transferFilters = transferFilters & Q(fromCategory__exact=request.POST['fromCategory'])
        if request.POST['toCategory'] != '':
            transferFilters = transferFilters & Q(toCategory__exact=request.POST['toCategory'])
        if request.POST['description'] != '':
            transferFilters = transferFilters & Q(description__exact=request.POST['description'])
        transferList = Transfers.objects.filter(transferFilters)
        # use filtered transfer list insted of this    transferList = Transfers.objects.all()
        if request.POST['timeSortType'] == 'Day':
            newList = list()
            for day, gByDay in itertools.groupby(transferList, key=lambda x: x.timestamp.day):
                sumOfAmounts = 0
                for i in gByDay:
                    sumOfAmounts += i.amount
                newList.append([sumOfAmounts, i.timestamp.date().strftime("%d/%m/%y")])
        form = filterForm(transferList, initial={
                                                "fromCategory": request.POST['fromCategory'],
                                                'toCategory': request.POST['toCategory']
                                                })
    else:
        transferList = Transfers.objects.filter(transferFilters)
        form = filterForm(transferList)
    # category sum
    fromCategorySum = Transfers.objects.values(
                                'fromCategory'
                                ).annotate(
                                sum_source=Sum('amount')
                                )
    categoryDict = dict()
    for iDict in fromCategorySum:
        categoryDict[iDict['fromCategory']] = iDict['sum_source']
    toCategorySum = Transfers.objects.values(
                                'toCategory'
                                ).annotate(
                                sum_dest=Sum('amount')
                                )
    for iDict in toCategorySum:
        if iDict['toCategory'] in categoryDict.keys():
            categoryDict[iDict['toCategory']] -= iDict['sum_dest']
        else:
            categoryDict[iDict['toCategory']] = -iDict['sum_dest']
    categoryTotalList = list()
    for key, value in categoryDict.iteritems():
        categoryTotalList.append([key, value])
    # insted of lambda fn you can use itemgetter
    categoryTotalList = sorted(categoryTotalList, key=lambda student: student[1], reverse = True)
    return render_to_response('personalTemplates/graph_N_list.html', locals(), context_instance=RequestContext(request))
