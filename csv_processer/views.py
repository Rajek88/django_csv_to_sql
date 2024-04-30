import os
import time
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend import settings

# Create your views here.
# here we will write our view


def say_hello(request):
    return HttpResponse("Hello")


@csrf_exempt
def upload_csv(request):
    current_time = round(time.time())
    if request.method == "POST":
        for key, file in request.FILES.items():
            path = os.path.join(
                settings.MEDIA_ROOT, "file_" + str(current_time) + "_" + file.name
            )
            with open(path, "wb") as dest:  # Open the file in binary mode
                if file.multiple_chunks():
                    for chunk in file.chunks():
                        dest.write(chunk)
                else:
                    dest.write(file.read())

        # Return a response object that indicates the success of the file upload.
        return JsonResponse({"message": "File uploaded successfully"}, status=200)
    else:
        return JsonResponse(
            {"message": "Please upload a file via post request"}, status=400
        )
