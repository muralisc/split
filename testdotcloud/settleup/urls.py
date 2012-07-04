from django.conf.urls.defaults import patterns, include, url
from TransactionsApp.views import PostsTableNotiListView, PostsTablePostListView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'settleup.TransactionsApp.views.login'),
    (r'^adduser/$', 'settleup.TransactionsApp.views.adduser'),
    (r'^displayusers/$', 'settleup.TransactionsApp.views.displayusers'),
    (r'^getTransaction/$', 'settleup.TransactionsApp.views.getTransaction'),
    (r'^displayTransactions/(\w+)/$', 'settleup.TransactionsApp.views.displayDetailedTransactions'),
    (r'^deleteTransactions/([-]?\d+)/$', 'settleup.TransactionsApp.views.deleteTransactions'),
    (r'^deleteUser/([-]?\d+)/$', 'settleup.TransactionsApp.views.deleteUser'),
    (r'^settleUP/$', 'settleup.TransactionsApp.views.settleUP'),
    (r'^fetchquote/$', 'settleup.TransactionsApp.views.fetchquote'),
    (r'^logout/$', 'settleup.TransactionsApp.views.logout'),
    (r'^posts/(\w+)/$', PostsTableNotiListView.as_view(template_name="noti.html")),
    (r'^showposts/(\w+)/$', PostsTablePostListView.as_view(template_name="posts.html")),
    (r'^getposts/$', 'settleup.TransactionsApp.views.Putpost'),
    (r'^download/$', 'settleup.TransactionsApp.views.downloadAsCsv'),
    (r'^calculator/(.*)/$', 'settleup.TransactionsApp.views.calculator'),

)
