from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.files.storage import FileSystemStorage

from .forms import UserBioForm, UploadFileForm

def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "...")
    b = request.GET.get("b", "...")
    c = a + ' + ' + b
    #e = 1/0
    context = {
        "a": a,
        "b": b,
        "c": c,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)



# def user_form(request: HttpRequest) -> HttpResponse:
#     return render(request, "requestdataapp/user-bio-form.html")
def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        "form": UserBioForm(),
    }
    return render(request, "requestdataapp/user-bio-form.html", context=context)



def user_file_upload(request: HttpRequest) -> HttpResponse:
    
    context = {
        "response_status": "upload nothing",        
    }        
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            
            myfile = request.FILES["myfile"]
            filename = myfile.name
            if myfile.size > 1024 * 10: # * 1024
                response_status = "Fail. File too big."
                print(filename, "fail to save")
            else:
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                print(filename, "saved")
                response_status = "Ok. File saved."
            context["response_status"] = response_status
    else:
        form = UploadFileForm()
        
    context["form"] = form
            
    return render(request, "requestdataapp/file-upload.html", context=context)

