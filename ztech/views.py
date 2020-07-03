from django.shortcuts import redirect
from django.http import HttpResponse

def index(request):    
    return redirect('/appcontrol/')

def test(request):
    return HttpResponse('This is a test function')
