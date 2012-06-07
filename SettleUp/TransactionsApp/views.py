# Create your views here.

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import django
from TransactionsApp.forms import addUserForm
from TransactionsApp.models import users

def login(request):
    return render_to_response('login.html','')


def useradd(request):
    form = addUserForm()
    return render_to_response('addUser.html',locals())


#@csrf_exempt
def addusertodb(request):
    form = addUserForm(request.POST)
    if form.is_valid():
        if users.objects.filter(username__exact = form.cleaned_data['username']).count() == 0:
            users.objects.create(
                    username = form.cleaned_data['username'],
                    password = form.cleaned_data['password'],
                    outstanding = 0
                    )
        else:
            cd = 'user aleady exist'
    else:
        cd = 'invalid form'
    return render_to_response('displayUser.html',locals(),context_instance = RequestContext(request))


def displayusers(request):
    dbrows = users.objects.all()
    return render_to_response('displayUser.html',locals(),context_instance = RequestContext(request))
    
