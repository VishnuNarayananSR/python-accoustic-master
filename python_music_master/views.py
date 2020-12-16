import os
from django.shortcuts import render 
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .backend.predict import predict
from django.http import JsonResponse
from time import sleep

def upload(request):
    if request.method == 'POST':
        sleep(3)
        try:
            myfile = request.FILES['audiofile']
        except:
            return JsonResponse("Didn't recieve any file!", safe=False)
        fs = FileSystemStorage()
        filepath = fs.save(os.path.join('media/',myfile.name), myfile)
        filename = os.path.basename(filepath)
        print(filename)
        result = predict(file_name=filename)
        return JsonResponse(result, safe=False)
        
    return render(request, 'index.html')