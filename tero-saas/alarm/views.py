import datetime
from base64 import b64decode
from io import BytesIO

from django.shortcuts import render
from django.core.files.images import ImageFile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from apps.alarm.forms import AlarmImageForm


@csrf_exempt
def save_image(request):
    b64image = request.POST.get('b64image')
    filename = request.POST.get('filename')
    alarm_id = request.POST.get('alarm_id')

    decoded = b64decode(b64image)
    image = BytesIO(decoded)

    form = AlarmImageForm(files={
        'image': ImageFile(image, name=filename)
    })

    if form.is_valid():
        image = form.save(commit=False)
        image.alarm_id = alarm_id
        image.save()
        
        return JsonResponse({ 
            'ok': True 
        })

    return JsonResponse(status=500, data={
        'ok': False,
        'errors': form.errors
    })
