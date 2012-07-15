from django.conf.urls.defaults import patterns, include, url
from TransactionsApp.views import DisplayPosts


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'settleup.TransactionsApp.views.login'),
    (r'^createUser/$', 'settleup.TransactionsApp.views.create_user'),
    (r'^changePassword/$', 'settleup.TransactionsApp.views.user_password_change'),
    (r'^displayusers/$', 'settleup.TransactionsApp.views.display_users'),
    (r'^createTransaction/$', 'settleup.TransactionsApp.views.create_transaction'),
    (r'^displayTransactions/(\w+)/$', 'settleup.TransactionsApp.views.display_transactions'),
    (r'^deleteTransactions/([-]?\d+)/$', 'settleup.TransactionsApp.views.delete_transactions'),
    (r'^deleteUser/([-]?\d+)/$', 'settleup.TransactionsApp.views.delete_user'),
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
)
