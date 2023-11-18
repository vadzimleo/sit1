from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
#request -> response
#request handler
#action
#what a client sees
def say_hello(request):
    #Pull data from db
    #Transform
    #Send email
    #return HttpResponse(' Hello world')
    #use template and return html-markup to the client
    #x = 1
    #y = 2
    return render(request, 'hello.html', {'name': 'Marie'})




