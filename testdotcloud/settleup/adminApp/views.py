# Django imports
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
#from TransactionsApp.forms import
from TransactionsApp.models import users, transactions, PostsTable
from adminApp.forms import EditUserForm


def admin_view(request):
    if users.objects.get(pk=request.session['sUserId']).username == 'admin':
        userFullName = 'admin'
    else:
        return redirect('/')
    usersTable = users.objects.all()
    transactionsTable = transactions.objects.all()
    postsTable = PostsTable.objects.order_by('PostType')
    return render_to_response('adminDB.html', locals(), context_instance=RequestContext(request))


def edit_user(request, usr_id):                    # {{{
    if users.objects.get(pk=request.session['sUserId']).username == 'admin':
        pass
    else:
        return redirect('/')
    usrToEdit = users.objects.get(id=usr_id)
    form = EditUserForm(request.POST or None, instance=usrToEdit)
    if request.method == 'POST':
        if form.is_valid():
                form.save()
                return redirect('/admin')
        else:
            pass
    return render_to_response('adminEditUser.html', locals(), context_instance=RequestContext(request))
                                         #}}}
