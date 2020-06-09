from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from core.models import ParametriGraficof, NaborGraficov


def render_main(request):
    nabor = NaborGraficov.objects.filter(skrit=False)
    return render(request, 'core/main.html', {
        'nabor': nabor
    })



def get_raschet(request):
    a = ParametriGraficof.objects.get(id=12).get_raschet()

    return HttpResponse(a)