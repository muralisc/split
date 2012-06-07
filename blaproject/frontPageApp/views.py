# Create your views here.
from django.shortcuts import render_to_response

def fp(request):
	return render_to_response('frontpage.html','')
def EnterData(request):
	limit = [0,1,2]
	return render_to_response('dataEntryPage.html',locals())
