from django.conf.urls.defaults import patterns, include, url
from TransactionsApp.views import DisplayNotifications, DisplayPosts


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'settleup.TransactionsApp.views.login'),
    (r'^createUser/$', 'settleup.TransactionsApp.views.create_user'),
    (r'^displayusers/$', 'settleup.TransactionsApp.views.display_users'),
    (r'^createTransaction/$', 'settleup.TransactionsApp.views.create_transaction'),
    (r'^displayTransactions/(\w+)/$', 'settleup.TransactionsApp.views.display_transactions'),
    (r'^deleteTransactions/([-]?\d+)/$', 'settleup.TransactionsApp.views.delete_transactions'),
    (r'^deleteUser/([-]?\d+)/$', 'settleup.TransactionsApp.views.delete_user'),
    (r'^settleUP/$', 'settleup.TransactionsApp.views.settle_grp'),
    (r'^fetchquote/$', 'settleup.TransactionsApp.views.fetch_quote'),
    (r'^logout/$', 'settleup.TransactionsApp.views.logout'),
    (r'^notifications/(\w+)/$', DisplayNotifications.as_view(template_name="noti.html")),
    (r'^displayPosts/(\w+)/$', DisplayPosts.as_view(template_name="posts.html")),
    (r'^createPost/$', 'settleup.TransactionsApp.views.create_post'),
    (r'^download/$', 'settleup.TransactionsApp.views.download_as_csv'),
    (r'^calculator/(.*)/$', 'settleup.TransactionsApp.views.calculator'),

)
