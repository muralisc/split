# Create your views here.
from django.shortcuts import render_to_response,redirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
#from TransactionsApp.forms import 
from TransactionsApp.models import users,transactions,transactionsForm,addUserForm,quotes
from TransactionsApp.forms import loginForm
import urllib
import pdb
import re
import random

def login(request):#{{{
    if 'memid' in request.session:              #request.session.get('memid',False):
        return redirect('/getTransaction')
    if request.method == 'POST':
        usrFromForm = loginForm(request.POST)
        if usrFromForm.is_valid():
            memberQuerySet = users.objects.filter(
            username__exact = usrFromForm.cleaned_data['username']
            ).filter(
            password__exact = usrFromForm.cleaned_data['password'])
            if memberQuerySet.count() == 0:
                login_msg = "Invalid username or password"
            else:
                request.session['memid'] = memberQuerySet[0].name
                return redirect('/getTransaction')
    form = loginForm()
    member_name = request.session['memid']
    return render_to_response('login.html',locals(),context_instance = RequestContext(request))
#}}}

def logout(request):  #{{{
    del request.session['memid']
    return redirect('/')
    #}}}

#@csrf_exempt
def adduser(request):                    #{{{
    if request.method == 'POST':
        form = addUserForm(request.POST)
        if form.is_valid():
            if users.objects.filter(username__exact = form.cleaned_data['username']).count() == 0:
                form.cleaned_data['outstanding']=0
                form.save()
                adduser_msg = "YIPEE!! User added.Login to continue"
            else:
                adduser_msg = "Username alredy exist. please chose a new one"
        else:
            pass
    form = addUserForm()
    member_name = request.session['memid']
    return render_to_response('addUser.html',locals(),context_instance = RequestContext(request))
                                         #}}}

def displayusers(request):              #{{{
    dbrows = users.objects.all()
    member_name = request.session['memid']
    return render_to_response('displayUser.html',locals(),context_instance = RequestContext(request))
#}}}

def getTransaction(request):     #{{{
    if request.method =='POST':
        form = transactionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/displayTransactions/all/')
    else:
        form = transactionsForm()
    member_name = request.session['memid']
    return render_to_response('transactionsGet.html',locals(),context_instance=RequestContext(request))
                                     #}}}

def displayDetailedTransactions(request,kind): #{{{
    userstable = users.objects.all()
    txnstable = transactions.objects.all()
    rows ={}
    for i in userstable:
        rows.update({i.username:0})                                     #make the sample row dict for table
    table= [dict(rows) for k in range(transactions.objects.count())]
    i=0
    for i,curtxn in enumerate(txnstable):                               #fetch each database row 
        if i==0:
            table[i][curtxn.user_paid.username] += curtxn.amount
            perpersoncost = curtxn.amount/curtxn.users_involved.count()
            for usrinv in curtxn.users_involved.all():
                table[i][usrinv.username] -= perpersoncost
        if i!=0:
            table[i][curtxn.user_paid.username] += curtxn.amount
            perpersoncost = curtxn.amount/curtxn.users_involved.count()
            for usrinv in curtxn.users_involved.all():
                table[i][usrinv.username] -= perpersoncost              #populatin "table" a list of dictionaries
    newtable = [list([None]*(len(userstable)*2+6)) for k in txnstable ] 
    for i,I in enumerate(table):
        for j,J in enumerate(userstable):
            if i==0:
                newtable[i][j+6] = table[i][J.username]
                newtable[i][j+len(userstable)+6] = table[i][J.username]
            else:
                newtable[i][j+6] = table[i][J.username]
                newtable[i][j+len(userstable)+6] = newtable[i][j+6] + newtable[i-1][j+len(userstable)+6]
    for i,row in enumerate(txnstable):
        newtable[i][0] = row.id
        newtable[i][1] = row.description
        newtable[i][2] = row.amount
        newtable[i][3] = row.user_paid
        newtable[i][4] = ''
        for ui_rows in row.users_involved.all():
            newtable[i][4] += ui_rows.username+' '
        newtable[i][5] = row.timestamp
    if cmp(kind,'all')==0:                                              #checking the url
        pass
    else:                                                               #else get transctions of user alone
        currentUser = users.objects.get(username=kind)
        txn_ids= currentUser.transactions_set1.values('id')             #get txn ids of involved
        txn_ids1= currentUser.transactions_set.values('id')             #get txn ids of paid
        txn_ids_list=[]
        for i in txn_ids:
            txn_ids_list.append(i['id'])
        for i in txn_ids1:
            txn_ids_list.append(i['id'])                                # make a txn_ids_list
        temp = newtable
        newtable =[]                                                    #make "new" newtable form newtable
        for i in temp:
            if i[0] in txn_ids_list:
                newtable.append(i)
    if len(newtable) != 0:
        for i,usr_row in enumerate(userstable):
            usr_row.outstanding = newtable[len(newtable)-1][6+len(userstable)+i]
            usr_row.save()                                                  # update the user table with the latest values
    ordered_userstable = users.objects.order_by('-outstanding')         # a ordered_userstable variable for link display in order
    member_name = request.session['memid']
    return render_to_response('displayDetailedTransactions.html',locals(),context_instance=RequestContext(request))
                                                   #}}}

def deleteTransactions(request,txn_id):#{{{
    if( int(txn_id) >=0 ):
        txnTOdelete = transactions.objects.get(id=txn_id)
        txnTOdelete.delete()
    all_txns = transactions.objects.all()
    member_name = request.session['memid']
    return render_to_response('deleteTransaction.html',locals(),context_instance=RequestContext(request))#}}}

def settleUP(request):  #{{{
    usr_details = users.objects.order_by('-outstanding')
    settleUPlist = []
    settleUPTextlist = []
    for i in usr_details:
        settleUPlist.append([i.username,i.outstanding])
    while (len(settleUPlist) != 1):
        n = len(settleUPlist)
        if( abs(settleUPlist[0][1])-abs(settleUPlist[n-1][1]) >=0 ):
            settleUPTextlist.append(settleUPlist[n-1][0]+'->'+settleUPlist[0][0]+' '+str(abs(settleUPlist[n-1][1])))
            settleUPlist[0][1] = abs(settleUPlist[0][1])-abs(settleUPlist[n-1][1])
            settleUPlist.pop()
        else:
            settleUPTextlist.append(settleUPlist[n-1][0]+'->'+settleUPlist[0][0]+' '+str(abs(settleUPlist[0][1])))
            settleUPlist[n-1][1] = abs(settleUPlist[0][1])-abs(settleUPlist[n-1][1])
            settleUPlist.pop(0)
        #sort the remainig list
        for j in range(0,len(settleUPlist)-1):
            temp = settleUPlist[j][1];
            loc = j
            for k in range(j+1,len(settleUPlist)-1):
                if(settleUPlist[k][1] > temp):
                    temp = settleUPlist[k][1]
                    loc = k
            temp = settleUPlist[loc]
            settleUPlist[loc] = settleUPlist[j]
            settleUPlist[j] = temp
    member_name = request.session['memid']
    return render_to_response('settleUP.html',locals(),context_instance=RequestContext(request))
                        #}}}

def fetchquote(request):#{{{

    data = urllib.urlopen('https://dl.dropbox.com/s/6tr3kur4826zwpy/quotes.txt').read()
    quoteslines = re.split('#',data)
    unshownQueryset = quotes.objects.filter(shown=0)
    if (quotes.objects.count() < len(quoteslines) or len(unshownQueryset) == 0):
        quotes.objects.all().delete()
        for i in quoteslines:
            a = quotes(q=i,shown= False )
            a.save()
    cur_quo_index = random.randint(0,len(unshownQueryset)-1)
    a = unshownQueryset[cur_quo_index].q
    unshownQueryset[cur_quo_index].shown =1
    unshownQueryset[cur_quo_index].save()
    member_name = request.session['memid']
    return render_to_response('index.html',locals(),context_instance = RequestContext(request))
#}}}

def deleteUser(request,usr_id):#{{{
    if( int(usr_id) >=0 ):
        usrTOdelete = users.objects.get(id=usr_id)
        usrTOdelete.delete()
    all_usrs = users.objects.all()
    member_name = request.session['memid']
    return render_to_response('deleteUser.html',locals(),context_instance=RequestContext(request))#}}}
#}}}


