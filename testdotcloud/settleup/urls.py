from django.conf.urls.defaults import patterns, include, url
from TransactionsApp.views import DisplayPosts


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'settleup.TransactionsApp.views.login'),
    (r'^createUser/$', 'settleup.TransactionsApp.views.create_user'),
    (r'^createGroup/$', 'settleup.TransactionsApp.views.create_group'),
    (r'^changePassword/$', 'settleup.TransactionsApp.views.user_password_change'),
    (r'^home/$', 'settleup.TransactionsApp.views.home_page'),
    (r'^tabClick/(\w+)/$', 'settleup.TransactionsApp.views.tab_click'),
    (r'^search/(\w+)/$', 'settleup.TransactionsApp.views.search'),
    (r'^groupHome/(\w+)/$', 'settleup.TransactionsApp.views.group_home_page'),
    (r'^displayusers/$', 'settleup.TransactionsApp.views.display_users'),
    (r'^transactions/(\w+)/$', 'settleup.TransactionsApp.views.transaction_create_display'),
    (r'^deleteTransactions/([-]?\d+)/$', 'settleup.TransactionsApp.views.delete_transactions'),
    (r'^deleteUser/([-]?\d+)/$', 'settleup.adminApp.views.delete_user'),
    (r'^settleUP/$', 'settleup.TransactionsApp.views.settle_grp'),
    (r'^fetchquote/$', 'settleup.TransactionsApp.views.fetch_quote'),
    (r'^logout/$', 'settleup.TransactionsApp.views.logout'),
    (r'^notifications/(\w+)/$', 'settleup.TransactionsApp.views.display_notifications'),
    (r'^displayPosts/(\w+)/$', DisplayPosts.as_view()),
    (r'^createPost/$', 'settleup.TransactionsApp.views.create_post'),
    (r'^download/$', 'settleup.TransactionsApp.views.download_as_csv'),
    (r'^calculator/(.*)/$', 'settleup.TransactionsApp.views.calculator'),
    (r'^admin/$', 'settleup.adminApp.views.admin_view'),
    (r'^admin/editUser/(\d+)/$', 'settleup.adminApp.views.edit_user'),
    (r'^admin/deletePost/(\d+)/$', 'settleup.adminApp.views.delete_post'),
    (r'^admin/deleteTxn/(\d+)/$', 'settleup.adminApp.views.delete_txn'),
)
