from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SettleUp.views.home', name='home'),
    # url(r'^SettleUp/', include('SettleUp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^$','SettleUp.TransactionsApp.views.login'),
    (r'^adduser/$','SettleUp.TransactionsApp.views.adduser'),
    (r'^addusertodb/$','SettleUp.TransactionsApp.views.addusertodb'),
    (r'^displayusers/$','SettleUp.TransactionsApp.views.displayusers'),
    (r'^getTransaction/$','SettleUp.TransactionsApp.views.getTransaction'),
    (r'^displayTransactions/(\w+)/$','SettleUp.TransactionsApp.views.displayTransactions'),
    
)
