from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    
    if request.session.get('user') is None:
        return redirect('/appcontrol/')
        
    user = request.session['user']
    return HttpResponse('Welcome to dashboard ' + user['first_name'] + ' ' + user['last_name'])
