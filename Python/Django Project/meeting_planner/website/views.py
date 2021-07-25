from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render

# Create your views here.

def welcome(request):
    return render(request,"website/welcome.html",{"mettings_number":"this is dynamic"})


def date(request):
    return HttpResponse("welcome to this website " + str(datetime.now()) )
