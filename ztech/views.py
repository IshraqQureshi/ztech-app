from django.shortcuts import redirect
from django.http import HttpResponse

def index(request):
    return redirect('/appcontrol/')