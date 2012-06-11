# Create your views here.
import pdb            #for set_trace()
from django.shortcuts import render_to_response,redirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
#from TransactionsApp.forms import 
from TransactionsApp.models import users,transactions,transactionsForm,addUserForm

def login(request):
    return render_to_response('login.html','')


def adduser(request):
    form = addUserForm()
    return render_to_response('addUser.html',locals())


#@csrf_exempt
def addusertodb(request):
    form = addUserForm(request.POST)
    if form.is_valid():
        if users.objects.filter(username__exact = form.cleaned_data['username']).count() == 0:
            form.save()
        else:
            cd = 'user aleady exist'
    else:
        cd = 'invalid form'
    return redirect('/displayusers/')


def displayusers(request):
    dbrows = users.objects.all()
    return render_to_response('displayUser.html',locals(),context_instance = RequestContext(request))
    
def getTransaction(request):
    form = transactionsForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/displayTransactions/all/')
    else:
        form = transactionsForm()
        return render_to_response('transactionsGet.html',locals(),context_instance=RequestContext(request))


def displayDetailedTransactions(request,kind):
    userstable = users.objects.all()
    txnstable = transactions.objects.all()
    rows ={}
    for i in userstable:
        rows.update({i.username:0})
    table= [dict(rows) for k in range(transactions.objects.count())]
    i=0
    for i,curtxn in enumerate(txnstable):
        if i==0:
            table[i][curtxn.user_paid.username] += curtxn.amount
            perpersoncost = curtxn.amount/curtxn.users_involved.count()
            for usrinv in curtxn.users_involved.all():
                table[i][usrinv.username] -= perpersoncost
        if i!=0:
            table[i][curtxn.user_paid.username] += curtxn.amount
            perpersoncost = curtxn.amount/curtxn.users_involved.count()
            for usrinv in curtxn.users_involved.all():
                table[i][usrinv.username] -= perpersoncost
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
    
    if cmp(kind,'all')==0:
        pass
    else:
        currentUser = users.objects.get(username=kind)
        txn_ids= currentUser.transactions_set1.values('id')
        txn_ids1= currentUser.transactions_set.values('id')
        txn_ids_list=[]
        for i in txn_ids:
            txn_ids_list.append(i['id'])
        for i in txn_ids1:
            txn_ids_list.append(i['id'])
        temp = newtable
        newtable =[]
        for i in temp:
            if i[0] in txn_ids_list:
                newtable.append(i)
#    pdb.set_trace()
    ordered_userstable = users.objects.order_by('-outstanding')
    for i,usr_row in enumerate(userstable):
        usr_row.outstanding = newtable[len(newtable)-1][6+len(userstable)+i]
        usr_row.save()
    return render_to_response('displayDetailedTransactions.html',locals(),context_instance=RequestContext(request))

