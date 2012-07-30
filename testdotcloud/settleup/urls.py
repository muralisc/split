from django.conf.urls.defaults import patterns


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'settleup.TransactionsApp.views.login'),
    (r'^admin/$', 'settleup.adminApp.views.admin_view'),
    (r'^admin/editUser/(\d+)/$', 'settleup.adminApp.views.edit_user'),
    (r'^admin/deletePost/(\d+)/$', 'settleup.adminApp.views.delete_post'),
    (r'^admin/deleteTxn/(\d+)/$', 'settleup.adminApp.views.delete_txn'),
    (r'^calculator/(.*)/$', 'settleup.TransactionsApp.views.calculator'),
    (r'^changePassword/$', 'settleup.TransactionsApp.views.user_password_change'),
    (r'^createGroup/$', 'settleup.TransactionsApp.views.create_group'),
    (r'^createPost/$', 'settleup.TransactionsApp.views.create_post'),
    (r'^createUser/$', 'settleup.TransactionsApp.views.create_user'),
    (r'^deleteTransactions/([-]?\d+)/$', 'settleup.TransactionsApp.views.delete_transactions'),
    (r'^deleteUser/([-]?\d+)/$', 'settleup.adminApp.views.delete_user'),
    (r'^displayPosts/(\w+)/$', 'settleup.TransactionsApp.views.display_posts'),
    (r'^displayusers/$', 'settleup.TransactionsApp.views.display_users'),
    (r'^download/$', 'settleup.TransactionsApp.views.download_as_csv'),
    (r'^fetchquote/$', 'settleup.TransactionsApp.views.fetch_quote'),
    (r'^groupHome/(\w+)/$', 'settleup.TransactionsApp.views.group_home_page'),
    (r'^home/$', 'settleup.TransactionsApp.views.home_page'),
    (r'^logout/$', 'settleup.TransactionsApp.views.logout'),
    (r'^notifications/(\w+)/$', 'settleup.TransactionsApp.views.display_notifications'),
    (r'^search/(\w+)/$', 'settleup.TransactionsApp.views.search'),
    (r'^settleUP/$', 'settleup.TransactionsApp.views.settle_grp'),
    (r'^tabClick/(\w+)/$', 'settleup.TransactionsApp.views.tab_click'),
    (r'^transactions/(\w+)/$', 'settleup.TransactionsApp.views.transaction_create_display'),
    (r'^transactionsInDetail/(\w+)/$', 'settleup.TransactionsApp.views.transaction_detail'),
    # --------------------------------------------------
    (r'^personalApp/fromCategory/$', 'settleup.personalApp.views.from_category_view'),
    (r'^personalApp/toCategory/$', 'settleup.personalApp.views.to_category_view'),
    (r'^personalApp/amount/$', 'settleup.personalApp.views.amount_view'),
    (r'^personalApp/description/$', 'settleup.personalApp.views.description_view'),
    (r'^personalApp/time/$', 'settleup.personalApp.views.time_view'),
    (r'^personalApp/summary/$', 'settleup.personalApp.views.summary'),
)
