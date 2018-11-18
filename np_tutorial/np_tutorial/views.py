from django.shortcuts import render


def home_page(request):
    context = {}
    return render(request, 'home_page.html', context)


def button_click(request):
    context = {
        'random_or_not': 1
    }
    return render(request, 'home_page.html', context)

