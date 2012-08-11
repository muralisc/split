import os
from optparse import OptionParser

usage = "usage: %prog -s SETTINGS | --settings=SETTINGS"
parser = OptionParser(usage)
parser.add_option('-s', '--settings', dest='settings', metavar='SETTINGS',
                  help="the django settings module to use")
(options, args) = parser.parse_args()
if not options.settings:
    parser.error("You must specify a settings module")

os.environ['DJANGO_SETTINGS_MODULE'] = options.settings

from TransactionsApp.models import transactions

for i in transactions.objects.all():
    temp = i
    temp.userPaidCost = i._get_user_paid_cost()
    temp.save()
print "done"
