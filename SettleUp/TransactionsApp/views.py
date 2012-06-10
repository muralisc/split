# Create your views here.

from django.shortcuts import render_to_response,redirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import django
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
        return redirect('/displayTransactions/one/')
    else:
        form = transactionsForm()
        return render_to_response('transactionsGet.html',locals(),context_instance=RequestContext(request))


def displayTransactions(request,kind):
    userdbrows = users.objects.all()
    if cmp(kind,'all')==0:
        dbrows = transactions.objects.all()
    return render_to_response('displayTransactions.html',locals(),context_instance=RequestContext(request))
