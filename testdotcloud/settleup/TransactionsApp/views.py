# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.views.generic import ListView
from django.template import RequestContext
from django.http import HttpResponse
#from TransactionsApp.forms import
from TransactionsApp.models import users, transactions, quotes, PostsTable
from TransactionsApp.forms import loginForm, transactionsForm, addUserForm, PostsForm
import urllib
import csv
import re
import datetime
import random


def login(request):  # {{{
    try:
        if request.session.get('memid', False):
            return redirect('/getTransaction')
    except KeyError:
        pass
    if request.method == 'POST':
        usrFromForm = loginForm(request.POST)
        if usrFromForm.is_valid():
            memberQuerySet = users.objects.filter(
            username__exact=usrFromForm.cleaned_data['username']
            ).filter(
            password__exact=usrFromForm.cleaned_data['password'])
            if memberQuerySet.count() == 0:
                login_msg = "Invalid username or password"
            else:
                request.session['memid'] = memberQuerySet[0].name
                request.session['memUsername'] = memberQuerySet[0].username
                return redirect('/getTransaction')
    form = loginForm()
    return render_to_response('login.html', locals(), context_instance=RequestContext(request))
    #}}}


def logout(request):  # {{{
    del request.session['memid']
    return redirect('/')
    #}}}


def adduser(request):                    # {{{
    if 'memid' not in request.session:
        return redirect('/')
    else:
        member_name = request.session['memid']
    if request.method == 'POST':
        form = addUserForm(request.POST)
        if form.is_valid():
            if users.objects.filter(username__exact=form.cleaned_data['username']).count() == 0:
                form.cleaned_data['outstanding'] = 0
                usr = form.save(commit=False)
                usr.outstanding = 0
                usr.lastNotiView = datetime.datetime.now()
                usr.save()
                adduser_msg = "YIPEE!! User added.Login to continue"
            else:
                adduser_msg = "Username alredy exist. please chose a new one"
        else:
            pass
    form = addUserForm()
    return render_to_response('addUser.html', locals(), context_instance=RequestContext(request))
                                         #}}}


def displayusers(request):              # {{{
    if 'memid' not in request.session:
        return redirect('/')
    else:
        member_name = request.session['memid']
    dbrows = users.objects.all()
    return render_to_response('displayUser.html', locals(), context_instance=RequestContext(request))
    #}}}


def getTransaction(request):     # {{{
    if 'memid' not in request.session:
        return redirect('/')
    else:
        member_name = request.session['memid']
    if request.method == 'POST':
        form = transactionsForm(request.POST)
        if form.is_valid():
            transactionsObj = form.save()
            postObject = PostsTable(
                            author=users.objects.get(name=member_name),
                            desc='added transaction',
                            linkToTransaction=transactions.objects.latest('timestamp'),
                            PostType='noti',
                                    )
            postObject.save()
            for usr in (transactionsObj.users_involved.all()):
                postObject.audience.add(usr)                     # should be added like this cause it need a primary id for ManyToManyField
            postObject.audience.add(transactionsObj.user_paid)
            return redirect('/displayTransactions/' + postObject.author.username + '/')
    else:
        form = transactionsForm()
    try:
        noOfNewNoti = PostsTable.objects.filter(
                                                timestamp__gte=users.objects.get(name=request.session['memid']).lastNotiView
                                                ).filter(
                                                PostType__exact='noti'
                                                ).filter(
                                                audience__in=[users.objects.get(name=request.session['memid']).id]
                                                ).order_by('-timestamp').count()
    except:
        noOfNewNoti = 0
    return render_to_response('transactionsGet.html', locals(), context_instance=RequestContext(request))
                                     #}}}


def displayDetailedTransactions(request, kind):   # {{{
    if 'memid' not in request.session:
        return redirect('/')
    else:
        member_name = request.session['memid']
    userstable = users.objects.all()
    txnstable = transactions.objects.filter(deleted__exact=False)
    rows = {}
    for i in userstable:
        rows.update({i.username: 0})                                     # make the sample row dict for table
    table = [dict(rows) for k in range(txnstable.count())]
    i = 0
    for i, curtxn in enumerate(txnstable):                               # fetch each database row
        if i == 0:
            table[i][curtxn.user_paid.username] += curtxn.amount
            perpersoncost = curtxn.amount / curtxn.users_involved.count()
            for usrinv in curtxn.users_involved.all():
                table[i][usrinv.username] -= perpersoncost
        if i != 0:
            table[i][curtxn.user_paid.username] += curtxn.amount
            perpersoncost = curtxn.amount / curtxn.users_involved.count()
            for usrinv in curtxn.users_involved.all():
                table[i][usrinv.username] -= perpersoncost              # populatin "table" a list of dictionaries
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
    if cmp(kind, 'all') == 0:                                              # checking the url
        if len(newtable) != 0:
            for i, usr_row in enumerate(userstable):
                usr_row.outstanding = newtable[len(newtable) - 1][6 + len(userstable) + i]
                usr_row.save()                                                  # update the user table with the latest values
    else:                                                               # else get transctions of user alone
        currentUser = users.objects.get(username=kind)
        txn_ids = currentUser.transactions_set1.values('id')             # get txn ids of involved
        txn_ids1 = currentUser.transactions_set.values('id')             # get txn ids of paid
        txn_ids_list = []
        for i in txn_ids:
            txn_ids_list.append(i['id'])
        for i in txn_ids1:
            txn_ids_list.append(i['id'])                                # make a txn_ids_list
        temp = newtable
        newtable = []                                                    # make "new" newtable form newtable
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
    ordered_userstable = users.objects.order_by('-outstanding')         # a ordered_userstable variable for link display in order
    request.session['downloadData'] = list(newtable)
    for i, I in enumerate(newtable):
        I[0] = i
    newtable.reverse()
    return render_to_response('displayDetailedTransactions.html', locals(), context_instance=RequestContext(request))
                                                   #}}}


def deleteTransactions(request, txn_id):    # {{{
    if 'memid' not in request.session:
        return redirect('/')
    else:
        member_name = request.session['memid']
    if(int(txn_id) >= 0):
        txnTOdelete = transactions.objects.get(id=txn_id)
        txnTOdelete.deleted = True
        txnTOdelete.save()
        postObject = PostsTable(
                        author=users.objects.get(name=member_name),
                        desc='deleted transaction',
                        linkToTransaction=transactions.objects.get(id=txn_id),
                        PostType='noti',
                                )
        postObject.save()
        for usr in (txnTOdelete.users_involved.all()):  # should be added like this cause it need a primary id for ManyToManyField
            postObject.audience.add(usr)
        postObject.audience.add(txnTOdelete.user_paid)
        return redirect('/deleteTransactions/-1/')
    all_txns = transactions.objects.filter(deleted__exact=False)
    return render_to_response('deleteTransaction.html', locals(), context_instance=RequestContext(request))
        # }}}


def settleUP(request):  # {{{
    if 'memid' not in request.session:
        return redirect('/')
    else:
        member_name = request.session['memid']
    usr_details = users.objects.order_by('-outstanding')
    settleUPlist = []
    settleUPTextlist = []
    for i in usr_details:
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


def fetchquote(request):  # {{{
    data = urllib.urlopen('https://dl.dropbox.com/s/6tr3kur4826zwpy/quotes.txt').read()
    data = unicode(data, "utf-8")
    data = data.encode('utf-8')
    quoteslines = re.split('#', data)
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
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))
    #}}}


def deleteUser(request, usr_id):  # {{{
    if 'memid' not in request.session:
        return redirect('/')
    else:
        member_name = request.session['memid']
    if(int(usr_id) >= 0):
        usrTOdelete = users.objects.get(id=usr_id)
        usrTOdelete.delete()
    all_usrs = users.objects.all()
    return render_to_response('deleteUser.html', locals(), context_instance=RequestContext(request))  # }}}
    #}}}


class PostsTableNotiListView(ListView):
    def get_queryset(self):
        if(self.args[0] == 'all'):
            return PostsTable.objects.order_by(
                                              '-timestamp'
                                              ).filter(
                                              PostType__exact='noti')

    def get_context_data(self, **kwargs):
        usr = users.objects.get(name=self.request.session['memid'])
        lsttime = usr.lastNotiView
        usr.lastNotiView = datetime.datetime.now()
        usr.save()
        context = super(PostsTableNotiListView, self).get_context_data(**kwargs)
        context['object_list_new'] = PostsTable.objects.filter(
                                                    timestamp__gte=lsttime
                                                    ).filter(
                                                    PostType__exact='noti'
                                                    ).filter(
                                                    audience__in=[usr.id]
                                                    ).order_by('-timestamp')
        context['noOfNewNoti'] = len(context['object_list_new'])
        context['member_name'] = usr.name
        return context


class PostsTablePostListView(ListView):
    def get_queryset(self):
        if(self.args[0] == 'all'):
            return PostsTable.objects.order_by('-timestamp').filter(PostType__exact='post')


# TODO consolidate the database
def Putpost(request):
    member_name = request.session['memid']
    if request.method == 'POST':
        form = PostsForm(request.POST)
        if form.is_valid():
            # we need to add the user data so we save the form without commit
            # so we get the obj to manipulate
            # http://stackoverflow.com/questions/7715263/whats-the-cleanest-way-to-add-arbitrary-data-to-modelform
            PostsTableObj = form.save(commit=False)
            PostsTableObj.author = users.objects.get(name=member_name)
            PostsTableObj.PostType = 'post'
            PostsTableObj.save()
            return redirect('/posts/all/')
    else:
        form = PostsForm()
    return render_to_response('getPost.html', locals(), context_instance=RequestContext(request))


def downloadAsCsv(request):
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
    if error != [""] and error != ['0']:
        result = error
    return HttpResponse(result)
