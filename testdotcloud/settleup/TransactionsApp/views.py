# Django imports
from django.shortcuts import render_to_response, redirect
from django.views.generic import ListView
from django.template import RequestContext
from django.http import HttpResponse
#from TransactionsApp.forms import
from TransactionsApp.models import users, transactions, quotes, PostsTable
from TransactionsApp.forms import loginForm, transactionsForm, addUserForm, PostsForm
# Python imports
import urllib
import csv
import re
import datetime
import random


def login(request):  # {{{
    try:
        if request.session.get('sUserFullname', False):
            return redirect('/createTransaction')
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
                request.session['sUserFullname'] = memberQuerySet[0].name
                return redirect('/createTransaction')
    form = loginForm()
    return render_to_response('login.html', locals(), context_instance=RequestContext(request))
    #}}}


def logout(request):  # {{{
    del request.session['sUserFullname']
    return redirect('/')
    #}}}


def create_user(request):                    # {{{
    # checking if logged in
    if 'sUserFullname' not in request.session:
        pass
    else:
        userFullName = request.session['sUserFullname']
    if request.method == 'POST':
        form = addUserForm(request.POST)
        if form.is_valid():
            if users.objects.filter(username__exact=form.cleaned_data['username']).count() == 0:
                form.cleaned_data['outstanding'] = 0
                currentUserObject = form.save(commit=False)
                currentUserObject.outstanding = 0
                currentUserObject.lastNotiView = datetime.datetime.now()
                currentUserObject.save()
                createUserPrompt = "User added.Login to continue"
            else:
                createUserPrompt = "Username alredy exist. please chose a new one"
        else:
            pass
    form = addUserForm()
    return render_to_response('addUser.html', locals(), context_instance=RequestContext(request))
                                         #}}}


def create_transaction(request):     # {{{
    """
    displays and process a new transaction form
    displays the number of new notifications
    makes and entry in the Posts table
    """
    if 'sUserFullname' not in request.session:
        return redirect('/')
    else:
        userFullName = request.session['sUserFullname']
    if request.method == 'POST':
        form = transactionsForm(request.POST)
        if form.is_valid():
            #retrieving the transactions object to populate the postObject field.
            transactionsObj = form.save()
            postObject = PostsTable(
                            author=users.objects.get(name=userFullName),
                            desc='added transaction',
                            linkToTransaction=transactions.objects.latest('timestamp'),
                            PostType='noti',
                                    )
            postObject.save()
            for usr in (transactionsObj.users_involved.all()):
                # should be added like this cause it need a primary id for ManyToManyField
                postObject.audience.add(usr)
            postObject.audience.add(transactionsObj.user_paid)
            return redirect('/displayTransactions/' + postObject.author.username + '/')
    else:
        form = transactionsForm()
    try:
        noOfNewNoti = PostsTable.objects.filter(
                                                timestamp__gte=users.objects.get(name=request.session['sUserFullname']).lastNotiView
                                                ).filter(
                                                PostType__exact='noti'
                                                ).filter(
                                                audience__in=[users.objects.get(name=request.session['sUserFullname']).id]
                                                ).order_by('-timestamp').count()
    except:
        noOfNewNoti = 0
    return render_to_response('transactionsGet.html', locals(), context_instance=RequestContext(request))
                                     #}}}


#========================================================
def display_users(request):              # {{{
    if 'sUserFullname' not in request.session:
        return redirect('/')
    else:
        userFullName = request.session['sUserFullname']
    usersDBrows = users.objects.all()
    displayType = "users"
    return render_to_response('display.html', locals(), context_instance=RequestContext(request))
    #}}}


class DisplayNotifications(ListView):
    template_name = "display.html"

    def get_queryset(self):
        if(self.args[0] == 'all'):
            return PostsTable.objects.order_by(
                                              '-timestamp'
                                              ).filter(
                                              PostType__exact='noti')

    def get_context_data(self, **kwargs):
        usr = users.objects.get(name=self.request.session['sUserFullname'])
        lsttime = usr.lastNotiView
        usr.lastNotiView = datetime.datetime.now()
        usr.save()
        context = super(DisplayNotifications, self).get_context_data(**kwargs)
        context['object_list_new'] = PostsTable.objects.filter(
                                                    timestamp__gte=lsttime
                                                    ).filter(
                                                    PostType__exact='noti'
                                                    ).filter(
                                                    audience__in=[usr.id]
                                                    ).order_by('-timestamp')
        context['noOfNewNoti'] = len(context['object_list_new'])
        context['userFullName'] = usr.name
        context['displayType'] = 'notifications'
        return context


class DisplayPosts(ListView):
    template_name = "display.html"

    def get_queryset(self):
        if(self.args[0] == 'all'):
            return PostsTable.objects.order_by('timestamp').filter(PostType__exact='post')

    def get_context_data(self, **kwargs):
        context = super(DisplayPosts, self).get_context_data(**kwargs)
        context['displayType'] = 'posts'
        context['userFullName'] = self.request.session['sUserFullname']
        return context


def display_transactions(request, kind):   # {{{
    if 'sUserFullname' not in request.session:
        return redirect('/')
    else:
        userFullName = request.session['sUserFullname']
    userstable = users.objects.all()
    txnstable = transactions.objects.filter(deleted__exact=False)
    rows = {}
    for i in userstable:
        # make the sample row dictionary for the "newtable"
        rows.update({i.username: 0})
    table = [dict(rows) for k in range(txnstable.count())]
    i = 0
    # fetch each database row
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
    # checking the url
    if cmp(kind, 'all') == 0:
        if len(newtable) != 0:
            for i, usr_row in enumerate(userstable):
                usr_row.outstanding = newtable[len(newtable) - 1][6 + len(userstable) + i]
                # update the user table with the latest values
                usr_row.save()
    # else get transctions of user alone
    else:
        currentUser = users.objects.get(username=kind)
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
            if j.username == kind:
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
    ordered_userstable = users.objects.order_by('-outstanding')
    request.session['downloadData'] = list(newtable)
    for i, I in enumerate(newtable):
        I[0] = i
    newtable.reverse()
    return render_to_response('displayDetailedTransactions.html', locals(), context_instance=RequestContext(request))
                                                  #}}}
#========================================================


def delete_transactions(request, txn_id):    # {{{
    if 'sUserFullname' not in request.session:
        return redirect('/')
    else:
        userFullName = request.session['sUserFullname']
    if(int(txn_id) >= 0):
        txnTOdelete = transactions.objects.get(id=txn_id)
        txnTOdelete.deleted = True
        txnTOdelete.save()
        postObject = PostsTable(
                        author=users.objects.get(name=userFullName),
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


def delete_user(request, usr_id):  # {{{
    if 'sUserFullname' not in request.session:
        return redirect('/')
    else:
        userFullName = request.session['sUserFullname']
    if(int(usr_id) >= 0):
        usrTOdelete = users.objects.get(id=usr_id)
        usrTOdelete.delete()
    usersDBrows = users.objects.all()
    deleteType = 'users'
    return render_to_response('delete.html', locals(), context_instance=RequestContext(request))  # }}}
     #}}}


def settle_grp(request):  # {{{
    if 'sUserFullname' not in request.session:
        return redirect('/')
    else:
        userFullName = request.session['sUserFullname']
    usersDBrows = users.objects.order_by('-outstanding')
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
def create_post(request):
    userFullName = request.session['sUserFullname']
    if request.method == 'POST':
        form = PostsForm(request.POST)
        if form.is_valid():
            # we need to add the user data so we save the form without commit
            # so we get the obj to manipulate
            # http://stackoverflow.com/questions/7715263/whats-the-cleanest-way-to-add-arbitrary-data-to-modelform
            PostsTableObj = form.save(commit=False)
            PostsTableObj.author = users.objects.get(name=userFullName)
            PostsTableObj.PostType = 'post'
            PostsTableObj.save()
            return redirect('/notifications/all/')
    else:
        form = PostsForm()
    return render_to_response('getPost.html', locals(), context_instance=RequestContext(request))


def download_as_csv(request):
    if 'downloadData' in request.session:
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
        newtable = request.session['downloadData']
        del request.session['downloadData']
        userstable = list(users.objects.all())
        writer = csv.writer(response)
        writer.writerow(["id", "DESCRIPTION", "AMOUNT", "PAID BY", "PAID FOR", "TIME"] + userstable + userstable)
        for i in range(len(newtable)):
            writer.writerow(newtable[i])
        return response
    else:
        return redirect('/displayTransactions/all/')


def calculator(request, exp):
    response = urllib.urlopen('http://www.google.com/ig/calculator?q=' + urllib.quote(exp))
    html = response.read()
    error = re.findall(r'error: "(.*?)"', html)
    result = re.findall(r'rhs: "([\d.]+)"', html)
    if error != [""] and error != ['0'] and error != ['4']:
        result = error
    return HttpResponse(result)
