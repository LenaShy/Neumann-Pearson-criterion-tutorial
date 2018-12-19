from django.shortcuts import render

from .forms import MatrixForm, ExcludeRowsForm, RightAnswerForm
from .models import Matrix

from decimal import Decimal


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
    matrix = MatrixForm()
    context['matrix'] = matrix
    if request.method == 'POST':
        matrix = Matrix.objects.last()
        context['threshold'] = round(matrix.threshold, 2)
        context['a11'] = matrix.a11
        context['a12'] = matrix.a12
        context['a21'] = matrix.a21
        context['a22'] = matrix.a22
        context['a31'] = matrix.a31
        context['a32'] = matrix.a32
        context.pop('matrix', None)
        context.pop('exclude_rows', None)
        if 'matrix' in request.POST:
            a11 = Decimal(request.POST.get('a11'))
            a12 = Decimal(request.POST.get('a12'))
            a21 = Decimal(request.POST.get('a21'))
            a22 = Decimal(request.POST.get('a22'))
            a31 = Decimal(request.POST.get('a31'))
            a32 = Decimal(request.POST.get('a32'))
            state = request.POST.get('state')
            context['controlled'] = state
            matrix = Matrix.objects.create(a11=a11, a12=a12, a21=a21, a22=a22, a31=a31, a32=a32, state=state)
            if state == 'state1':
                threshold = (a11 + a21 + a31) / 3
                if a11 > threshold:
                    matrix.exclude_alpha1 = True
                if a21 > threshold:
                    matrix.exclude_alpha2 = True
                if a31 > threshold:
                    matrix.exclude_alpha3 = True
            else:
                threshold = (a12 + a22 + a32) / 3
                if a12 > threshold:
                    matrix.exclude_alpha1 = True
                if a22 > threshold:
                    matrix.exclude_alpha2 = True
                if a32 > threshold:
                    matrix.exclude_alpha3 = True
            matrix.threshold = threshold
            matrix.save()
            context['threshold'] = round(threshold, 2)
            context['a11'] = a11
            context['a12'] = a12
            context['a21'] = a21
            context['a22'] = a22
            context['a31'] = a31
            context['a32'] = a32
            context['exclude_rows'] = ExcludeRowsForm()
        if 'exclude_rows' in request.POST:
            exclude_rows = ExcludeRowsForm(request.POST)
            context['exclude_rows'] = exclude_rows
            if ('row1' in request.POST and matrix.exclude_alpha1 is not True
                or 'row1' not in request.POST and matrix.exclude_alpha1 is True) \
                    or ('row2' in request.POST and matrix.exclude_alpha2 is not True
                        or 'row2' not in request.POST and matrix.exclude_alpha2 is True) \
                    or ('row3' in request.POST and matrix.exclude_alpha3 is not True
                        or 'row3' not in request.POST and matrix.exclude_alpha3 is True):
                context['message'] = 'Вы ошиблись!'
            else:
                context['message'] = 'Правильный ответ!'
            context['right_answer'] = RightAnswerForm()
        if 'right_answer' in request.POST:
            pass
    '''if request.method == "POST":
        if 'matrix' in request.POST:
            matrix = Matrix(request.POST)
            state = request.POST.get('state')
            if state == 'select1':
                threshold = (Decimal(request.POST.get('a11')) + Decimal(request.POST.get('a21'))
                             + Decimal(request.POST.get('a31'))) / 3
            else:
                threshold = (Decimal(request.POST.get('a12')) + Decimal(request.POST.get('a22'))
                             + Decimal(request.POST.get('a32'))) / 3
            if matrix.is_valid():
                matrix.save()
            context['matrix'] = matrix
            context['threshold'] = round(threshold, 2)
            exclude_rows = ExcludeRowsForm()
            context['exclude_rows'] = exclude_rows
        if 'exclude_rows' in request.POST:
            exclude_rows = ExcludeRowsForm(request.POST)
            context['exclude_rows'] = exclude_rows

    else:
        matrix = Matrix()
        context['matrix'] = matrix'''

    return render(request, 'training_for_nrandom.html', context)
