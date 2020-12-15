import os
from django.shortcuts import render 
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .backend.predict import predicttest
from time import sleep
def upload(request):
    if request.method == 'POST':
        try:
            myfile = request.FILES['audiofile']
        except:
            return render(request, 'prediction.html', {
            'result': ["Didn't recieve any file!"]
            })
        fs = FileSystemStorage()
        filename = fs.save(os.path.join('media/',myfile.name), myfile)
        result = predicttest(file_name=filename)
        return render(request, 'prediction.html', {
            'result': result
        })
    return render(request, 'index.html')

# def prediction(request):
#         return render(request, 'prediction.html', {'result': result})
    # else:
    #     form = UploadFileForm()
    # return render(request, 'upload.html', {'form': form})