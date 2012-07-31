# Django imports
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.sessions.models import Session
#from TransactionsApp.forms import
from TransactionsApp.models import users, transactions, PostsTable, GroupsTable
from adminApp.forms import EditUserForm


def admin_view(request):
    if 'sUserId' not in request.session:
        return redirect('/')
    if users.objects.get(pk=request.session['sUserId']).username == 'admin':
        userFullName = 'admin'
    else:
        return redirect('/')
    usersTable = users.objects.order_by('-lastLogin')
    transactionsTable = transactions.objects.all()
    postsTable = PostsTable.objects.order_by('PostType')
    groupsTable = GroupsTable.objects.all()
    sessionsTable = Session.objects.all()
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


def delete_user(request, usr_id):  # {{{ TODO refine transacions and outstanding field
    if users.objects.get(pk=request.session['sUserId']).username == 'admin':
        pass
    else:
        return redirect('/')
    if(int(usr_id) >= 0):
        usrTOdelete = users.objects.get(id=usr_id)
        usrTOdelete.delete()
    return redirect('/admin')
     #}}}


def delete_post(request, post_id):  # {{{
    if users.objects.get(pk=request.session['sUserId']).username == 'admin':
        pass
    else:
        return redirect('/')
    if(int(post_id) >= 0):
        postTOdelete = PostsTable.objects.get(id=post_id)
        postTOdelete.delete()
    return redirect('/admin')
     #}}}


def delete_txn(request, txn_id):  # {{{
    if users.objects.get(pk=request.session['sUserId']).username == 'admin':
        pass
    else:
        return redirect('/')
    if(int(txn_id) >= 0):
        txnTOdelete = transactions.objects.get(id=txn_id)
        txnTOdelete.delete()
    return redirect('/admin')
     #}}}
