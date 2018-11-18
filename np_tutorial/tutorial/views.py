from django.shortcuts import render


def theory_for_random(request):
    return render(request, 'theory_for_random.html', {})
