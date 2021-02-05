from django.shortcuts import render
from time import sleep
def index(request):
    sleep(5)
    return render(request, 'example/index.html')