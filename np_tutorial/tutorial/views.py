from django.shortcuts import render
from django.http import JsonResponse

from .forms import MatrixForm, RowsForm
from .models import Matrix

import math
import random


def training_for_random(request):
    context = {}
    matrix_form = MatrixForm()
    context['matrix_form'] = matrix_form
    if request.method == 'POST':
        #context.pop('exclude_rows', None)
        #context.pop('answer', None)
        # this part works when there are no input
        context.pop('matrix_form', None)
        if 'matrix_input' in request.POST:
            a11 = float(request.POST.get('a11'))
            a12 = float(request.POST.get('a12'))
            a21 = float(request.POST.get('a21'))
            a22 = float(request.POST.get('a22'))
            a31 = float(request.POST.get('a31'))
            a32 = float(request.POST.get('a32'))
            state = request.POST.get('state')
            context['controlled'] = state
            matrix = Matrix.objects.create(a11=a11, a12=a12, a21=a21, a22=a22, a31=a31, a32=a32, state=state)
            threshold = 0
            if state == '\\(\\beta_{1}\\)':
                answer = [0 for i in range(3)]
                losses = 0
                threshold = round(random.uniform(min([a11, a21, a31]) - 1, max([a11, a21, a31]) + 1), 2)
                l1 = [a11, a21, a31]
                l2 = [a12, a22, a32]
                minl2 = min(l2)
                minl2_index = l2.index(minl2)
                clean_l1_idnex = []
                dirty_l1_index = []
                for item in l1:
                    if item < threshold:
                        clean_l1_idnex.append(l1.index(item))
                        if l2[l1.index(item)] == minl2_index:
                            answer[minl2_index] = 1
                    else:
                        dirty_l1_index.append(l1.index(item))
                if clean_l1_idnex:
                    min_dirty_l1_index = l1.index(min([l1[index] for index in dirty_l1_index]))
                    min_clean_l2_index = l2.index(min([l2[index] for index in clean_l1_idnex]))
                    x = (threshold - l1[min_dirty_l1_index])/(l1[min_clean_l2_index] - l1[min_dirty_l1_index])
                    answer[min_clean_l2_index] = x
                    answer[min_dirty_l1_index] = 1 - x
                    losses = x * l2[min_clean_l2_index] + (1 - x) * l2[min_dirty_l1_index]

            elif state == '\\(\\beta_{2}\\)':
                threshold = random.uniform(min([a12, a22, a32]) - 1, max([a12, a22, a32]) + 1)
            matrix.threshold = threshold
            matrix.save()
            context['threshold'] = threshold
            context['a11'] = a11
            context['a12'] = a12
            context['a21'] = a21
            context['a22'] = a22
            context['a31'] = a31
            context['a32'] = a32
            context['exclude_rows'] = RowsForm()
        else:
            # this part works when there are no input
            matrix = Matrix.objects.last()
            if matrix is not None:
                context['threshold'] = round(matrix.threshold, 2)
                context['controlled'] = matrix.state
                context['a11'] = matrix.a11
                context['a12'] = matrix.a12
                context['a21'] = matrix.a21
                context['a22'] = matrix.a22
                context['a31'] = matrix.a31
                context['a32'] = matrix.a32
        if 'exclude_rows' in request.POST:
            context['exclude_rows'] = RowsForm(request.POST)
            if ('row1' in request.POST and matrix.exclude_alpha1 is not True
                or 'row1' not in request.POST and matrix.exclude_alpha1 is True) \
                    or ('row2' in request.POST and matrix.exclude_alpha2 is not True
                        or 'row2' not in request.POST and matrix.exclude_alpha2 is True) \
                    or ('row3' in request.POST and matrix.exclude_alpha3 is not True
                        or 'row3' not in request.POST and matrix.exclude_alpha3 is True):
                context['message1'] = 'Вы ошиблись!'
                context['color'] = 'color: red;'
            else:
                context['message1'] = 'Правильный ответ!'
                context['color'] = 'color: green;'
                context['answer'] = RowsForm()
    return render(request, 'training_for_random.html', context)


def example_for_random(request):
    return render(request, 'example_for_random.html', {})


def theory_for_random(request):
    return render(request, 'theory_for_random.html', {})


def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data)


def example_for_nrandom(request):
    return render(request, 'example_for_nrandom.html', {})


def training_for_nrandom(request):
    context = {}
    matrix = MatrixForm()
    context['matrix'] = matrix
    if request.method == 'POST':
        matrix = Matrix.objects.last()
        if matrix is not None:
            context['threshold'] = round(matrix.threshold, 2)
            context['controlled'] = matrix.state
            context['a11'] = matrix.a11
            context['a12'] = matrix.a12
            context['a21'] = matrix.a21
            context['a22'] = matrix.a22
            context['a31'] = matrix.a31
            context['a32'] = matrix.a32
            context.pop('matrix', None)
            context.pop('exclude_rows', None)
            context.pop('answer', None)
        if 'matrix' in request.POST:
            a11 = float(request.POST.get('a11'))
            a12 = float(request.POST.get('a12'))
            a21 = float(request.POST.get('a21'))
            a22 = float(request.POST.get('a22'))
            a31 = float(request.POST.get('a31'))
            a32 = float(request.POST.get('a32'))
            state = request.POST.get('state')
            context['controlled'] = state
            matrix = Matrix.objects.create(a11=a11, a12=a12, a21=a21, a22=a22, a31=a31, a32=a32, state=state)
            threshold = 0
            if state == '\\(\\beta_{1}\\)':
                threshold = (a11 + a21 + a31) / 3
                if a11 > threshold:
                    matrix.exclude_alpha1 = True
                if a21 > threshold:
                    matrix.exclude_alpha2 = True
                if a31 > threshold:
                    matrix.exclude_alpha3 = True
                answer_list = [a12, a22, a32]
                min_row = min(answer_list)
                if min_row < threshold:
                    matrix.losses = min_row
                    i = 0
                    for answer in answer_list:
                        i += 1
                        if answer == min_row:
                            matrix.answer_nrand.append(i)
            elif state == '\\(\\beta_{2}\\)':
                threshold = (a12 + a22 + a32) / 3
                if a12 > threshold:
                    matrix.exclude_alpha1 = True
                if a22 > threshold:
                    matrix.exclude_alpha2 = True
                if a32 > threshold:
                    matrix.exclude_alpha3 = True
                answer_list = [a11, a21, a31]
                min_row = min(answer_list)
                if min_row < threshold:
                    matrix.losses = min_row
                    i = 0
                    for answer in answer_list:
                        i += 1
                        if answer == min_row:
                            matrix.answer_nrand.append(i)
            matrix.threshold = threshold
            matrix.save()
            context['threshold'] = round(threshold, 2)
            context['a11'] = a11
            context['a12'] = a12
            context['a21'] = a21
            context['a22'] = a22
            context['a31'] = a31
            context['a32'] = a32
            context['exclude_rows'] = RowsForm()
        if 'exclude_rows' in request.POST:
            context['exclude_rows'] = RowsForm(request.POST)
            if ('row1' in request.POST and matrix.exclude_alpha1 is not True
                or 'row1' not in request.POST and matrix.exclude_alpha1 is True) \
                    or ('row2' in request.POST and matrix.exclude_alpha2 is not True
                        or 'row2' not in request.POST and matrix.exclude_alpha2 is True) \
                    or ('row3' in request.POST and matrix.exclude_alpha3 is not True
                        or 'row3' not in request.POST and matrix.exclude_alpha3 is True):
                context['message1'] = 'Вы ошиблись!'
                context['color'] = 'color: red;'
            else:
                context['message1'] = 'Правильный ответ!'
                context['color'] = 'color: green;'
                context['answer'] = RowsForm()
        if 'answer' in request.POST:
            context['answer'] = RowsForm(request.POST)
            if ('row1' in request.POST and 1 not in matrix.answer_nrand
                or 'row1' not in request.POST and 1 in matrix.answer_nrand) \
                    or ('row2' in request.POST and 2 not in matrix.answer_nrand
                        or 'row2' not in request.POST and 2 in matrix.answer_nrand) \
                    or ('row3' in request.POST and 3 not in matrix.answer_nrand
                        or 'row3' not in request.POST and 3 in matrix.answer_nrand ):
                context['message2'] = 'Вы ошиблись!'
                context['color'] = 'color: red;'
            else:
                context['message2'] = 'Правильный ответ!'
                context['color'] = 'color: green;'
                context['losses'] = RowsForm()
        if 'losses' in request.POST:
            context['losses'] = RowsForm(request.POST)
            losses = request.POST.get('case_losses')
            if math.isclose(float(losses), matrix.losses, abs_tol=0.001):
                context['end_of_tutorial'] = True
            else:
                context['message3'] = 'Вы ошиблись!'
                context['color'] = 'color: red;'
    return render(request, 'training_for_nrandom.html', context)
