import asyncio

from django.http import HttpResponse
from .service import pythonftx


def index(request):
    pythonftx.run()
    return HttpResponse('ok')
