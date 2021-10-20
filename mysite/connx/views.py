from django.http.response import FileResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import FileForm
import os
import subprocess
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_protect,csrf_exempt

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
            #Covert the file to PNG
            files = request.FILES.getlist('file')
            file_name = files[0].name.split('.')
            print(file_name)
            # data = get_data(files[0])
            # rect1, rect2, rect3, ax1, ax2, ax3 = draw_barth(data)
            # save_pitcure(rect1, rect2, rect3, ax1, ax2, ax3, data, file_name)
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
            path = "python -m onnx_connx "+ "upload/"+file_name[0] +".onnx "
            print(path)
            out = subprocess.run(path, shell=True, check= True,capture_output=True,text=True)
            return redirect('view')
    else:
        form = FileForm()
        return render(request, 'upload.html', locals())

def png_viewer(request):
    #file_name = request.session['file_name']
    
    file_name= "model.connx"
    
    return render(request, 'file_list.html', {'file_name': file_name})

def download_view(request):
    #file_name = request.session['file_name']
    """
    Download the Connx Model
    """
    #file_result = FileModel.objects.filter(id=id)
    '''
    if file_result:

        file = list(file_result)[0]

        # 文件名称及路径
        name = file.name
        path = file.path

        # 读取文件
        file = open(path, 'rb')
        response = FileResponse(file)

        # 使用urlquote对文件名称进行编码
        response[
            'Content-Disposition'] = 'attachment;filename="%s"' % urlquote(
                name)
    '''
    name = "model.connx"  #file.name
    path = "out/model.connx"  #file.path
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
