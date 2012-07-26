# Django imports
from django.shortcuts import render_to_response, redirect
from django.views.generic import ListView
from django.template import RequestContext
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Sum
#from TransactionsApp.forms import
from TransactionsApp.models import users, transactions, quotes, PostsTable, GroupsTable
from TransactionsApp.forms import loginForm, transactionsForm, addUserForm, PostsForm, PasswordChangeForm, GroupForm
# Python imports
import urllib
import csv
import re
import random
import datetime
from json import JSONEncoder
import itertools


def login(request):  # {{{
    try:
        if request.session.get('sUserId', False):
            userFullName = users.objects.get(pk=request.session['sUserId']).name
            return redirect('/transactions/' + userFullName)
    except KeyError:
        pass
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            memberQuerySet = users.objects.filter(
            username__exact=form.cleaned_data['username']
            ).filter(
            password__exact=form.cleaned_data['password'])
            if memberQuerySet.count() == 0:
                loginMessage = "Invalid username or password"
            else:
                request.session['sUserId'] = memberQuerySet[0].id
                loggedInUser = memberQuerySet[0]
                loggedInUser.lastLogin = datetime.datetime.now()
                loggedInUser.save()
                if memberQuerySet[0].name == 'admin':
                    return redirect('/admin')
                else:
                    return redirect('/transactions/' + loggedInUser.name)
    form = loginForm()
    return render_to_response('login.html', locals(), context_instance=RequestContext(request))
    #}}}


def logout(request):  # {{{
    if request.session.get('sUserId', False):
        del request.session['sUserId']
        return redirect('/')
    else:
        return redirect('/')
    #}}}


def create_user(request):                    # {{{
    if request.method == 'POST':
        form = addUserForm(request.POST)
        if form.is_valid():
            # if another user with the same username does not exist
            if users.objects.filter(username__exact=form.cleaned_data['username']).count() == 0:
                form.cleaned_data['outstanding'] = 0
                currentUserObject = form.save(commit=False)
                currentUserObject.outstanding = 0
                try:
                    # assign the latest notification
                    currentUserObject.lastNotification = PostsTable.objects.filter(
                                                            PostType__exact='noti'
                                                            ).latest('id')
                except:
                    currentUserObject.lastNotification = None
                try:
                    currentUserObject.lastPost = PostsTable.objects.filter(
                                                            PostType__exact='post'
                                                            ).latest('id')
                except:
                    currentUserObject.lastPost = None
                currentUserObject.lastLogin = datetime.datetime.now()
                currentUserObject.save()
                createUserPrompt = "User added.Login to continue"
            else:
                createUserPrompt = "Username alredy exist. please chose a new one"
        else:
            pass
    form = addUserForm()
    return render_to_response('addUser.html', locals(), context_instance=RequestContext(request))
                                         #}}}


def create_post(request):   # {{{
    if 'sUserId' not in request.session:
        return redirect('/')
    userFullName = users.objects.get(pk=request.session['sUserId']).name
    loggedInUser = users.objects.get(pk=request.session['sUserId'])
    if request.method == 'POST':
        form = PostsForm(loggedInUser, request.POST)
        if form.is_valid():
            # we need to add the user data so we save the form without commit
            # so we get the obj to manipulate
            # http://stackoverflow.com/questions/7715263/whats-the-cleanest-way-to-add-arbitrary-data-to-modelform
            PostsTableObj = form.save(commit=False)
            PostsTableObj.author = loggedInUser
            PostsTableObj.PostType = 'post'
            PostsTableObj.save()
            form.save_m2m()
            PostsTableObj.audience.add(loggedInUser)
            # update user object
            loggedInUser.lastPost = PostsTableObj
            loggedInUser.save()
            return redirect('/displayPosts/all/')
    else:
        form = PostsForm(loggedInUser)
    return render_to_response('getPost.html', locals(), context_instance=RequestContext(request))
        # }}}
#========================================================


def display_users(request):              # {{{
    if 'sUserId' not in request.session:
        return redirect('/')
    else:
        userFullName = users.objects.get(pk=request.session['sUserId']).name
    usersDBrows = users.objects.filter(deleted__exact=False).order_by("-outstanding")
    displayType = "users"
    loggedInUser = users.objects.get(pk=request.session['sUserId'])
    return render_to_response('display.html', locals(), context_instance=RequestContext(request))
    #}}}


def display_notifications(request, *args):    # {{{
    if 'sUserId' not in request.session:
        return redirect('/')
    loggedInUser = users.objects.get(pk=request.session['sUserId'])
    if(args[0] == 'all'):
        object_list = PostsTable.objects.filter(
                                            id__lte=loggedInUser.lastNotification.id
                                            ).filter(
                                            PostType__exact='noti'
                                            ).filter(
                                            audience__in=[loggedInUser.id]
                                            ).order_by(
                                            '-id'
                                            )
    if(loggedInUser.lastNotification):
        object_list_new = PostsTable.objects.filter(
                                            id__gt=loggedInUser.lastNotification.id
                                            ).filter(
                                            PostType__exact='noti'
                                            ).filter(
                                            audience__in=[loggedInUser.id]
                                            ).order_by(
                                            '-id'
                                            )
        noOfNewNoti = len(object_list_new)
    try:
        loggedInUser.lastNotification = PostsTable.objects.filter(
                                                PostType__exact='noti'
                                                ).latest('id')
    except PostsTable.DoesNotExist:
        pass
    loggedInUser.save()
    displayType = 'notifications'
    userFullName = users.objects.get(pk=request.session['sUserId']).name
    return render_to_response('display.html', locals(), context_instance=RequestContext(request))
            # }}}


#login controll left TODO
class DisplayPosts(ListView):  # {{{
    template_name = "display.html"

    def get_queryset(self):
        loggedInUser = users.objects.get(pk=self.request.session['sUserId'])
        if(self.args[0] == 'all'):
            return PostsTable.objects.order_by(
                                                '-timestamp'
                                              ).filter(
                                                PostType__exact='post'
                                              ).filter(
                                              audience__in=[loggedInUser.id]
                                              )

    def get_context_data(self, **kwargs):
        loggedInUser = users.objects.get(pk=self.request.session['sUserId'])
        context = super(DisplayPosts, self).get_context_data(**kwargs)
        if(loggedInUser.lastPost):
            context['object_list_new'] = PostsTable.objects.filter(
                                                        id__gt=loggedInUser.lastPost.id
                                                        ).filter(
                                                        PostType__exact='post'
                                                        ).filter(
                                                        audience__in=[loggedInUser.id]
                                                        )
        try:
            loggedInUser.lastPost = PostsTable.objects.filter(
                                                    PostType__exact='post'
                                                    ).latest('id')
        except PostsTable.DoesNotExist:
            pass
        loggedInUser.save()
        context['displayType'] = 'posts'
        context['userFullName'] = users.objects.get(pk=self.request.session['sUserId']).name
        return context
    # }}}


#========================================================


def delete_transactions(request, txn_id):    # {{{
    if 'sUserId' not in request.session:
        return redirect('/')
    else:
        userFullName = users.objects.get(pk=request.session['sUserId']).name
        loggedInUser = users.objects.get(id=request.session['sUserId'])
    if(int(txn_id) >= 0):
        txnTOdelete = transactions.objects.get(id=txn_id)
        txnTOdelete.deleted = True
        #outstanding field
        involvedList = list(txnTOdelete.users_involved.all())
        if txnTOdelete.user_paid in involvedList:
            for anyUsr in involvedList:
                if anyUsr != txnTOdelete.user_paid:
                    anyUsr.outstanding = anyUsr.outstanding + txnTOdelete.perpersoncost
                    anyUsr.save()
                else:
                    txnTOdelete.user_paid.outstanding = txnTOdelete.user_paid.outstanding - txnTOdelete.amount + txnTOdelete.perpersoncost
                    txnTOdelete.user_paid.save()
        else:
            for anyUsr in involvedList:
                anyUsr.outstanding = anyUsr.outstanding + txnTOdelete.perpersoncost
                anyUsr.save()
            txnTOdelete.user_paid.outstanding = txnTOdelete.user_paid.outstanding - txnTOdelete.amount
            txnTOdelete.user_paid.save()
        txnTOdelete.save()
        postObject = PostsTable(
                        author=users.objects.get(pk=request.session['sUserId']),
                        desc='deleted transaction',
                        linkToTransaction=transactions.objects.get(id=txn_id),
                        PostType='noti',
                                )
        postObject.save()
        for usr in (txnTOdelete.users_involved.all()):  # should be added like this cause it need a primary id for ManyToManyField
            postObject.audience.add(usr)
        postObject.audience.add(txnTOdelete.user_paid)
        return redirect('/deleteTransactions/-1/')
    txnsDBrows = transactions.objects.filter(deleted__exact=False)
    deleteType = 'transactions'
    return render_to_response('delete.html', locals(), context_instance=RequestContext(request))
        # }}}


def settle_grp(request):  # {{{
    if 'sUserId' not in request.session:
        return redirect('/')
    else:
        userFullName = users.objects.get(pk=request.session['sUserId']).name
    loggedInUser = users.objects.get(pk=request.session['sUserId'])
    usersDBrows = users.objects.filter(deleted__exact=False).order_by('-outstanding')
    settleUPlist = []
    settleUPTextlist = []
    for i in usersDBrows:
        settleUPlist.append([i.username, i.outstanding])
    while (len(settleUPlist) != 1):
        n = len(settleUPlist)
        if(abs(settleUPlist[0][1]) - abs(settleUPlist[n - 1][1]) >= 0):
            settleUPTextlist.append(settleUPlist[n - 1][0] + '->' + settleUPlist[0][0] + ' ' + str(abs(settleUPlist[n - 1][1])))
            settleUPlist[0][1] = abs(settleUPlist[0][1]) - abs(settleUPlist[n - 1][1])
            settleUPlist.pop()
        else:
            settleUPTextlist.append(settleUPlist[n - 1][0] + '->' + settleUPlist[0][0] + ' ' + str(abs(settleUPlist[0][1])))
            settleUPlist[n - 1][1] = abs(settleUPlist[0][1]) - abs(settleUPlist[n - 1][1])
            settleUPlist.pop(0)
        #sort the remainig list
        for j in range(0, len(settleUPlist) - 1):
            temp = settleUPlist[j][1]
            loc = j
            for k in range(j + 1, len(settleUPlist) - 1):
                if(settleUPlist[k][1] > temp):
                    temp = settleUPlist[k][1]
                    loc = k
            temp = settleUPlist[loc]
            settleUPlist[loc] = settleUPlist[j]
            settleUPlist[j] = temp
    return render_to_response('settleUP.html', locals(), context_instance=RequestContext(request))
                        #}}}


def fetch_quote(request):  # {{{
    htmlData = urllib.urlopen('https://dl.dropbox.com/s/6tr3kur4826zwpy/quotes.txt').read()
    htmlData = unicode(htmlData, "utf-8")
    htmlData = htmlData.encode('utf-8')
    quoteslines = re.split('#', htmlData)
    unshownQueryset = quotes.objects.filter(shown=0)
    if (quotes.objects.count() < len(quoteslines) or len(unshownQueryset) == 0):
        quotes.objects.all().delete()
        for i in quoteslines:
            a = quotes(q=i, shown=False)
            a.save()
    cur_quo_index = random.randint(0, len(unshownQueryset) - 1)
    a = unshownQueryset[cur_quo_index].q
    unshownQueryset[cur_quo_index].shown = 1
    unshownQueryset[cur_quo_index].save()
    return render_to_response('quotes.html', locals(), context_instance=RequestContext(request))
    #}}}


# TODO consolidate the database
# create a logs table
# user settings

def download_as_csv(request):   # {{{
    if request.session.get('sUserId', False):
        userFullName = users.objects.get(pk=request.session['sUserId']).name
    else:
        return redirect('/')
    if 'downloadData' in request.session:
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
        newtable = request.session['downloadData']
        del request.session['downloadData']
        userstable = list(users.objects.filter(deleted__exact=False).all())
        writer = csv.writer(response)
        writer.writerow(["id", "DESCRIPTION", "AMOUNT", "PAID BY", "PAID FOR", "TIME"] + userstable + userstable)
        for i in range(len(newtable)):
            writer.writerow(newtable[i])
        return response
    else:
        return redirect('/displayTransactions/all/')
            # }}}


def calculator(request, exp):       # {{{
    response = urllib.urlopen('http://www.google.com/ig/calculator?q=' + urllib.quote(exp))
    html = response.read()
    error = re.findall(r'error: "(.*?)"', html)
    result = re.findall(r'rhs: "(.*?)"', html)
    result = re.sub('\xa0', '', result[0])
    if error != [""] and error != ['0'] and error != ['4']:
        result = error
    return HttpResponse(result)
        # }}}


def user_password_change(request):                    # {{{
    # checking if logged in
    if request.session.get('sUserId', False):
        userFullName = users.objects.get(pk=request.session['sUserId']).name
    else:
        return redirect('/')
    loggedInUser = users.objects.get(id=request.session['sUserId'])
    form = PasswordChangeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if loggedInUser.password == form.cleaned_data['oldPassword']:
                loggedInUser.password = form.cleaned_data['newPassword']
                loggedInUser.save()
                return redirect('/')  # TODO go to user profile
            else:
                userPrompt = "wrong old password"
        else:

            pass
    return render_to_response('userPasswordChange.html', locals(), context_instance=RequestContext(request))
                                         #}}}


def home_page(request):
    if request.session.get('sUserId', False):
        userFullName = users.objects.get(pk=request.session['sUserId']).name
        loggedInUser = users.objects.get(pk=request.session['sUserId'])
    else:
        return redirect('/')
    user_groups = loggedInUser.groupsTable_members.all()
    return render_to_response('home.html', locals(), context_instance=RequestContext(request))


def group_home_page(request, grp):
    if request.session.get('sUserId', False):
        userFullName = users.objects.get(pk=request.session['sUserId']).name
        loggedInUser = users.objects.get(pk=request.session['sUserId'])
    else:
        return redirect('/')
    user_groups = loggedInUser.groupsTable_members.all()
    if request.method == 'POST':
        for i in request.POST['invites'].split(','):
            # make approval logic
            current_group.members.add(users.objects.get(pk=i))
    return render_to_response('groupHome.html', locals(), context_instance=RequestContext(request))


def create_group(request):
    if 'sUserId' not in request.session:
        return redirect('/')
    userFullName = users.objects.get(pk=request.session['sUserId']).name
    loggedInUser = users.objects.get(pk=request.session['sUserId'])
    if request.method == 'POST':
        form = GroupForm(request.POST or None)
        if form.is_valid():
            currentObject = form.save(commit=False)
            currentObject.save()
            currentObject.members.add(loggedInUser)
            currentObject.adimns.add(loggedInUser)
            createPrompt = "Group created"
    form = GroupForm(None)
    return render_to_response('createGroup.html', locals(), context_instance=RequestContext(request))


def transaction_create_display(request, kind):
    """
    displays and process a new transaction form
    displays the number of new notifications
    makes and entry in the Posts table
    updates outstanding column in usertable
    """
    if 'sUserId' not in request.session:
        return redirect('/')
    else:
        userFullName = users.objects.get(pk=request.session['sUserId']).name
    if request.method == 'POST':
        form = transactionsForm(request.POST)
        if form.is_valid():
            # retrieving the transactions object to populate the postObject field and the perpersoncost field
            transactionsObj = form.save()
            # perpersoncost field
            transactionsObj.perpersoncost = transactionsObj.amount / transactionsObj.users_involved.count()
            transactionsObj.save()
            # outdtanding field
            involvedList = list(transactionsObj.users_involved.all())
            if transactionsObj.user_paid in involvedList:
                for anyUsr in involvedList:
                    if anyUsr != transactionsObj.user_paid:
                        anyUsr.outstanding = anyUsr.outstanding - transactionsObj.perpersoncost
                        anyUsr.save()
                    else:
                        transactionsObj.user_paid.outstanding = transactionsObj.user_paid.outstanding + transactionsObj.amount - transactionsObj.perpersoncost
                        transactionsObj.user_paid.save()
            else:
                for anyUsr in involvedList:
                    anyUsr.outstanding = anyUsr.outstanding - transactionsObj.perpersoncost
                    anyUsr.save()
                transactionsObj.user_paid.outstanding = transactionsObj.user_paid.outstanding + transactionsObj.amount
                transactionsObj.user_paid.save()
            postObject = PostsTable(
                            author=users.objects.get(pk=request.session['sUserId']),
                            desc='added transaction',
                            linkToTransaction=transactions.objects.latest('timestamp'),
                            PostType='noti',
                                    )
            postObject.save()
            # 'loggedinuser' is put here because it interfears with the save
            # operation at updating the user objects outstanding field
            loggedInUser = users.objects.get(pk=request.session['sUserId'])
            loggedInUser.lastNotification = postObject
            loggedInUser.save()
            for user in (transactionsObj.users_involved.all()):
                # should be added like this cause it need a primary id for ManyToManyField
                postObject.audience.add(user)
            postObject.audience.add(transactionsObj.user_paid)
            return redirect('/transactions/' + userFullName + '/')
    else:
        # for a fresh load of url
        loggedInUser = users.objects.get(pk=request.session['sUserId'])
        form = transactionsForm()
        try:
            noOfNewNoti = PostsTable.objects.filter(
                                                    id__gt=users.objects.get(pk=request.session['sUserId']).lastNotification.id
                                                    ).filter(
                                                    PostType__exact='noti'
                                                    ).filter(
                                                    audience__in=[users.objects.get(pk=request.session['sUserId']).id]
                                                    ).count()
        except:
            if PostsTable.objects.count() > 0 and loggedInUser.lastNotification == None:
                loggedInUser.lastNotification = PostsTable.objects.latest('id')
                loggedInUser.save()
            noOfNewNoti = 0
        try:
            noOfNewPosts = PostsTable.objects.filter(
                                                    id__gt=users.objects.get(pk=request.session['sUserId']).lastPost.id
                                                    ).filter(
                                                    PostType__exact='post'
                                                    ).filter(
                                                    audience__in=[users.objects.get(pk=request.session['sUserId']).id]
                                                    ).count()
        except:
            if PostsTable.objects.count() > 0 and loggedInUser.lastPost == None:
                loggedInUser.lastPost = PostsTable.objects.latest('id')
                loggedInUser.save()
            noOfNewPosts = 0
    userstable = users.objects.filter(deleted__exact=False)
    txnstable = transactions.objects.filter(deleted__exact=False)
    rows = {}
    for i in userstable:
        # make the sample row dictionary for the "newtable"
        rows.update({i.username: 0})
    table = [dict(rows) for k in range(txnstable.count())]
    i = 0
    # fetch each transaction database row
    for i, curtxn in enumerate(txnstable):
        if i == 0:
            table[i][curtxn.user_paid.username] += curtxn.amount
            perpersoncost = curtxn.amount / curtxn.users_involved.count()
            for usrinv in curtxn.users_involved.all():
                table[i][usrinv.username] -= perpersoncost
        if i != 0:
            table[i][curtxn.user_paid.username] += curtxn.amount
            perpersoncost = curtxn.amount / curtxn.users_involved.count()
            for usrinv in curtxn.users_involved.all():
                # populating "table" a list of dictionaries
                table[i][usrinv.username] -= perpersoncost
    newtable = [list([None] * (len(userstable) * 2 + 6)) for k in txnstable]
    for i, I in enumerate(table):
        for j, J in enumerate(userstable):
            if i == 0:
                newtable[i][j + 6] = table[i][J.username]
                newtable[i][j + len(userstable) + 6] = table[i][J.username]
            else:
                newtable[i][j + 6] = table[i][J.username]
                newtable[i][j + len(userstable) + 6] = newtable[i][j + 6] + newtable[i - 1][j + len(userstable) + 6]
    for i, row in enumerate(txnstable):
        newtable[i][0] = row.id
        newtable[i][1] = row.description
        newtable[i][2] = row.amount
        newtable[i][3] = row.user_paid
        newtable[i][4] = ''
        for ui_rows in row.users_involved.all():
            newtable[i][4] += ui_rows.username + ' '
        newtable[i][5] = row.timestamp
    request.session['downloadData'] = list(newtable)
    # checking the url
    if cmp(kind, 'all') == 0:
        pass
    # else get transctions of user alone
    else:
        currentUser = users.objects.get(name=kind)
        # get txn ids of involved
        txn_ids = currentUser.transactions_set1.values('id')
        # get txn ids of paid
        txn_ids1 = currentUser.transactions_set.values('id')
        txn_ids_list = []
        for i in txn_ids:
            txn_ids_list.append(i['id'])
        for i in txn_ids1:
            # make a txn_ids_list
            txn_ids_list.append(i['id'])
        temp = newtable
        # make "new" newtable form newtable
        newtable = []
        userpos = 0
        for j in userstable:
            if j.name == kind:
                userpos = userpos + 1
                break
            userpos = userpos + 1
        usercount = len(userstable)
        for i in temp:
            if i[0] in txn_ids_list:
                t = i[0:6]
                t.append(i[5 + userpos])
                t.append(i[5 + userpos + usercount])
                newtable.append(t)
    # a ordered_userstable variable for link display in order
    outstanding_userstable = users.objects.filter(deleted__exact=False).order_by('-outstanding')
    # calculate actual expenditure.
    actual_expenditure = list()
    for usr in outstanding_userstable:
        aaa = usr.transactions_set1.aggregate(Sum('perpersoncost'))['perpersoncost__sum']
        if aaa != None:
            actual_expenditure.append(aaa)
        else:
            actual_expenditure(0)
    ordered_userstable = zip(outstanding_userstable, actual_expenditure)
    for i, I in enumerate(newtable):
        I[0] = i
    newtable.reverse()
    # integrity checks
    sumOfAllOutstanding = 0
    for j in userstable:
        sumOfAllOutstanding = sumOfAllOutstanding + j.outstanding
    return render_to_response('transactions.html', locals(), context_instance=RequestContext(request))


def search(request, kind):
    if kind == 'users':
        searchQuery = request.GET['q']
        resultQuerySet = users.objects.filter(Q(name__icontains=searchQuery) | Q(username__icontains=searchQuery))
        resultList = list()
        for res in itertools.chain(resultQuerySet):
            resultList.append({"id": res.pk, "name": res.name})
        result = JSONEncoder().encode(resultList)
        return HttpResponse(result)
    if kind == 'groups':
        searchQuery = request.GET['query']
        resultQuerySet = GroupsTable.objects.filter(Q(name__icontains=searchQuery))
        resultSuggession = list()
        resultData = list()
        for res in itertools.chain(resultQuerySet):
            resultSuggession.append(res.name)
            resultData.append(res.pk)
        resultDict = {
                        'query': searchQuery,
                        'suggestions': resultSuggession,
                        'data': resultData
                    }
        result = JSONEncoder().encode(resultDict)
        return HttpResponse(result)


# TODO convet posts table to prompts table
# TODO convet adimns to admins
# TODO convet user groups to foregin key

def tab_click(request, grp_id):
    loggedInUser = users.objects.get(pk=request.session['sUserId'])
    try:
        current_group = GroupsTable.objects.get(pk=grp_id)
        loggedInUser.groups.clear()
        loggedInUser.groups.add(current_group)
        loggedInUser.save()
    except:
        return redirect('/')
    return HttpResponse("done")
