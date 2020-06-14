from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.
from django.views.decorators.csrf import csrf_exempt


class ErshAPiView():

    def __init__(self):
        pass

    @csrf_exempt
    def dispatch(self, request):
        if request.method == 'GET':
            response = self.get(request)
            return response

        if request.method == 'POST':
            response = self.post(request)
            return response

    def get(self, request):
        return(HttpResponse('<h1>Ersh Api View</h1>'))
    
    def post(self, request):
        print(request)
        return(JsonResponse(200))