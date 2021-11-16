from django.http.response import FileResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import FileForm
import os
import subprocess
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import shutil



# Create your views here.
@csrf_exempt
def upload_file(request):
    return render(request, 'upload.html', locals())
    
@csrf_exempt
def index(request):
    """
    upload File
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            #Get Files
            files = request.FILES.getlist('file')
            file_name = files[0].name.split('.')
            
            # request.session['file_name'] = file_name
            

            # save the file in database or local server
            for file in files:
                # save in database through the model
                #  file_model = FileModel(name=file.name,
                #                         path=os.path.join(
                #                             './upload', file.name))
                #  file_model.save()

                # Save the file in local server
                destination = open(os.path.join("./upload", file.name), 'wb+')
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()

            #Using the Onnx_Connx Molde to get Connx File
            if not os.path.exists("./out"):
                path = "python -m onnx_connx "+ "./upload/"+file_name[0] +".onnx "
                subprocess.run(path, shell=True, check= True,capture_output=True,text=True)

                # Compressed Files 
                shutil.make_archive("out",'zip', "out")
            else:
                shutil.rmtree("./out")
                path = "python -m onnx_connx "+ "./upload/"+file_name[0] +".onnx"
                subprocess.run(path, shell=True, check= True,capture_output=True,text=True)

                # Compressed Files 
                shutil.make_archive("out",'zip', "out")         

            return redirect('download')
    else:
        form = FileForm()
        return render(request, 'upload.html', locals())

"""
Download the Connx Model
"""
def download_view(request):
    #file_name = request.session['file_name']
    name = "out.zip"  #file.name
    path = "./out.zip"  #file.path
    File_exists = os.path.exists(path)

    if File_exists == True:

        # Read the File
        file = open(path, 'rb')

        response = FileResponse(file)

        # Coding the File's name in  urlquote
        response[
            'Content-Disposition'] = 'attachment;filename="%s"' % urlquote(
                name)
        # Session.objects.all().delete()

        return response

    else:
        return HttpResponse('No Files')
