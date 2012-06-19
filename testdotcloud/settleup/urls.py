from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'settleup.views.home', name='home'),
    # url(r'^settleup/', include('SettleUp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
    (r'^$','settleup.TransactionsApp.views.login'),
    (r'^adduser/$','settleup.TransactionsApp.views.adduser'),
    (r'^displayusers/$','settleup.TransactionsApp.views.displayusers'),
    (r'^getTransaction/$','settleup.TransactionsApp.views.getTransaction'),
    (r'^displayTransactions/(\w+)/$','settleup.TransactionsApp.views.displayDetailedTransactions'),
    (r'^deleteTransactions/([-]?\d+)/$','settleup.TransactionsApp.views.deleteTransactions'),
    (r'^settleUP/$','settleup.TransactionsApp.views.settleUP'),
    (r'^fetchquote/$','settleup.TransactionsApp.views.fetchquote'),

    
)
