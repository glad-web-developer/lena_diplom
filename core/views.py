from django.shortcuts import render

# Create your views here.
from core.models import ParametriGraficof, NaborGraficov


def render_main(request):
    nabor = NaborGraficov.objects.filter(skrit=False)
    return render(request, 'core/main.html', {
        'nabor': nabor
    })
