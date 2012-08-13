# Django imports
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.db.models import Count, Sum
from django.db.models import Q
# app imports
from personalApp.models import Transfers, Categories
from TransactionsApp.models import users
from personalApp.forms import transferForm, filterForm, CreateCategory
# Python imports
import datetime
import itertools
# TODO user support for pf


def from_category_view(request):
    if 'sUserId' not in request.session:
        return redirect('/')
    else:
        loggedInUser = users.objects.get(pk=request.session['sUserId'])
    if request.method == "POST":
        form = transferForm(request.POST)
        if form.is_valid():
            if 'fromSelected' in request.POST:
                currentTransfer = Transfers()
                currentTransfer.fromCategory_id = request.POST['fromSelected']
                request.session['currentTransfer'] = currentTransfer
                return redirect('/personalApp/toCategory/')
            if form.cleaned_data['fromCategory'] != '':
                request.session['newCategory'] = form.cleaned_data['fromCategory']
                request.session['nextLink'] = '/personalApp/toCategory/'
                return redirect('/personalApp/createCategory/')
            else:
                errors = "enter some category"
    else:
        form = transferForm()
        fromDistinct = Categories.objects.filter(
                                    userID=loggedInUser.pk,
                                    category_type='source'
                                    )
    return render_to_response('personalTemplates/fromSelect.html', locals(), context_instance=RequestContext(request))


def to_category_view(request):
    if 'sUserId' not in request.session:
        return redirect('/')
    else:
        loggedInUser = users.objects.get(pk=request.session['sUserId'])
    if 'currentTransfer' not in request.session:
        return redirect('/personalApp/fromCategory/')
    else:
        if request.method == "POST":
            form = transferForm(request.POST)
            if form.is_valid():
                if 'toSelected' in request.POST:
                    currentTransfer = request.session['currentTransfer']
                    currentTransfer.toCategory_id = request.POST['toSelected']
                    request.session['currentTransfer'] = currentTransfer
                    return redirect('/personalApp/amount/')
                if form.cleaned_data['toCategory'] != '':
                    request.session['newCategory'] = form.cleaned_data['toCategory']
                    request.session['nextLink'] = '/personalApp/amount/'
                    return redirect('/personalApp/createCategory/')
                else:
                    errors = "enter some category"
        else:
            form = transferForm()
            currentTransfer = request.session['currentTransfer']
            toDistinct = Categories.objects.filter(
                                    userID=loggedInUser.pk,
                                    category_type='leach'
                                    )
            fromDistinct = Categories.objects.filter(
                                        userID=loggedInUser.pk,
                                        category_type='source'
                                        )
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
        else:
            form = transferForm()
            currentTransfer = request.session['currentTransfer']
    return render_to_response('personalTemplates/timeSelect.html', locals(), context_instance=RequestContext(request))


def summary(request):
    if 'sUserId' not in request.session:
        return redirect('/')
    else:
        loggedInUser = users.objects.get(pk=request.session['sUserId'])
    if 'currentTransfer' not in request.session:
        return redirect('/personalApp/fromCategory/')
    else:
        currentTransfer = request.session['currentTransfer']
        # if request.method == "POST":
        currentTransfer.userID = loggedInUser.pk
        currentTransfer.save()
        if 'currentTransfer' in request.session:
            del request.session['currentTransfer']
        if 'newCategory' in request.session:
            del request.session['newCategory']
        if 'nextLink' in request.session:
            del request.session['nextLink']
        return redirect('/personalApp/fromCategory/')


def statistics(request):
    if 'sUserId' not in request.session:
        return redirect('/')
    else:
        loggedInUser = users.objects.get(pk=request.session['sUserId'])
    transferFilters = Q(userID=loggedInUser.pk)
    if request.method == "POST":
        if 'delete' in request.POST:
            xferIdToDelete = request.POST['delete']
            Transfers.objects.get(pk=xferIdToDelete).delete()
        # filter the data based in the filters
        if request.POST['fromCategory'] != '' and request.POST['fromCategory'] != 'CWS':
            transferFilters = transferFilters & Q(fromCategory_id=request.POST['fromCategory'])
        elif request.POST['fromCategory'] == 'CWS':
            transferFilters = transferFilters & Q(fromCategory_id__in=[x for (x,) in Categories.objects.filter(category_type='source').values_list('id')])
        if request.POST['toCategory'] != '' and request.POST['toCategory'] != 'CWS':
            transferFilters = transferFilters & Q(toCategory_id=request.POST['toCategory'])
        elif request.POST['toCategory'] == 'CWS':
            transferFilters = transferFilters & Q(toCategory_id__in=[x for (x,) in Categories.objects.filter(category_type='leach').values_list('id')])
        if request.POST['description'] != '':
            transferFilters = transferFilters & Q(description__exact=request.POST['description'])
        if request.POST['timeSortType'] == 'Day':
            transferFilters = transferFilters & Q(toCategory_id__in=[x for (x,) in Categories.objects.filter(category_type='leach').values_list('id')])
        form = filterForm(None, request.POST)
        if form.is_valid():
            if request.POST['timeStart'] != '':
                transferFilters = transferFilters & Q(timestamp__gte=form.cleaned_data['timeStart'])
            if request.POST['timeEnd'] != '':
                transferFilters = transferFilters & Q(timestamp__lt=form.cleaned_data['timeEnd'] + datetime.timedelta(days=1))
        transferList = Transfers.objects.filter(transferFilters)
        totalAmount = transferList.aggregate(Sum('amount'))['amount__sum']
        # use filtered transfer list insted of this    transferList = Transfers.objects.all()
        if request.POST['timeSortType'] == 'Day':
            newList = list()
            for day, gByDay in itertools.groupby(transferList, key=lambda x: x.timestamp.day):
                sumOfAmounts = 0
                for i in gByDay:
                    sumOfAmounts += i.amount
                newList.append([sumOfAmounts, i.timestamp.date().strftime("%b %d, %Y")])
        if request.POST['toCategory'] == 'CWS':
            cwsToList = list()
            for i in transferList.values('toCategory').annotate(amt=Sum('amount')):
                cwsToList.append([Categories.objects.get(pk=i['toCategory']).name, i['amt']])
        if request.POST['fromCategory'] == 'CWS':
            cwsFromList = list()
            for i in transferList.values('fromCategory').annotate(amt=Sum('amount')):
                cwsFromList.append([Categories.objects.get(pk=i['fromCategory']).name, i['amt']])
        categoryList = Categories.objects.filter(
                                    userID=loggedInUser.pk,
                                    )
        form = filterForm(categoryList, initial={
                                                "fromCategory": request.POST['fromCategory'],
                                                'toCategory': request.POST['toCategory'],
                                                'timeSortType': request.POST['timeSortType'],
                                                'timeStart': request.POST['timeStart'],
                                                'timeEnd': request.POST['timeEnd'],
                                                })
    else:
        categoryList = Categories.objects.filter(
                                    userID=loggedInUser.pk,
                                    )
        form = filterForm(categoryList)
    # category sum--------------------------------------
    fromCategorySum = Transfers.objects.values(
                                'fromCategory_id'
                                ).annotate(
                                sum_source=Sum('amount')
                                )
    categoryDict = dict()
    for iDict in fromCategorySum:
        categoryDict[iDict['fromCategory_id']] = -iDict['sum_source']
    toCategorySum = Transfers.objects.filter(
                                ~Q(toCategory_id__in=[x for (x,) in Categories.objects.filter(category_type='leach').values_list('id')])
                                ).values(
                                'toCategory_id'
                                ).annotate(
                                sum_dest=Sum('amount')
                                )
    for iDict in toCategorySum:
            categoryDict[iDict['toCategory_id']] += iDict['sum_dest']
    for i in categoryList:
        if i.pk in categoryDict:
            categoryDict[i.pk] += i.initial_amt
        else:
            categoryDict[i.pk] = i.initial_amt
    categorySourceList = list()
    sourceList = Categories.objects.filter(userID=loggedInUser.pk, category_type='source').values('id')
    for key, value in categoryDict.iteritems():
        if {'id': key} in sourceList:
            categorySourceList.append([Categories.objects.get(pk=key).name, value])
    # insted of lambda fn you can use itemgetter
    categorySourceList = sorted(categorySourceList, key=lambda x: x[1], reverse=True)
    return render_to_response('personalTemplates/graph_N_list.html', locals(), context_instance=RequestContext(request))


def create_category_view(request):
    form = CreateCategory({'name': request.session['newCategory'], 'initial_amt': 0})
    if request.method == 'POST':
        form = CreateCategory(request.POST)
        if form.is_valid():
            categoryObject = form.save(commit=False)
            categoryObject.userID = users.objects.get(pk=request.session['sUserId']).pk
            categoryObject.save()
            if request.session['nextLink'] == '/personalApp/amount/':
                currentTransfer = request.session['currentTransfer']
                currentTransfer.toCategory_id = categoryObject.pk
                request.session['currentTransfer'] = currentTransfer
            if request.session['nextLink'] == '/personalApp/toCategory/':
                currentTransfer = Transfers()
                currentTransfer.toCategory_id = categoryObject.pk
                request.session['currentTransfer'] = currentTransfer
            return redirect(request.session['nextLink'])
    return render_to_response('personalTemplates/createCategory.html', locals(), context_instance=RequestContext(request))
