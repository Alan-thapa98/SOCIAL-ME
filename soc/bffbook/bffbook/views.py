from django.http import HttpResponse
from django.shortcuts import render
from time import time
from datetime import datetime


def home_view(request):
    user = request.user
    hello = 'Welocme:'
    # time = time.time('%d-%m-%Y')
    localtime = datetime.now()
    context = {
        'user': user,
        'hello': hello,
        'localtime': localtime,
    }
    return render(request, 'main/home.html', context)

    # return HttpResponse('Hello world')


