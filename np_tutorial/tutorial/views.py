from django.shortcuts import render

from .forms import Matrix


def theory_for_random(request):
    matrix = Matrix()
    context = {
        'matrix': matrix,
    }
    return render(request, 'theory_for_random.html', context)


def example_for_nrandom(request):
    return render(request, 'example_for_nrandom.html', {})


def training_for_nrandom(request):
    context = {}
    if request.GET.get('q'):
        matrix = Matrix(int(request.GET.get('q')))
        context = {
            'matrix': matrix,
        }
    return render(request, 'training_for_nrandom.html', context)
