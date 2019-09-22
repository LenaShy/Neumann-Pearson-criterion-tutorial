from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.forms import modelform_factory

from .forms import MatrixForm, RowsForm
from .models import Matrix, Row

import math
import random


def temp_decision_handling(l1, l2):
    answer = [0 for i in range(3)]
    losses = 0
    threshold = round(random.uniform(min(l1) - 1, max(l2) + 1), 2)
    '''minl2 = min(l2)
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
        x = (threshold - l1[min_dirty_l1_index]) / (l1[min_clean_l2_index] - l1[min_dirty_l1_index])
        answer[min_clean_l2_index] = x
        answer[min_dirty_l1_index] = 1 - x
        losses = x * l2[min_clean_l2_index] + (1 - x) * l2[min_dirty_l1_index]'''
    return answer, losses, threshold


'''def training_for_random(request):
    context = {}
    matrix_form = MatrixForm(5)
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
                l1 = [a11, a21, a31]
                l2 = [a12, a22, a32]
                answer, losses, threshold = temp_decision_handling(l1, l2)

            elif state == '\\(\\beta_{2}\\)':
                pass
            matrix.threshold = threshold
            matrix.save()
            context['matrix'] = matrix
            #context['exclude_rows'] = RowsForm()
            #return HttpResponseRedirect(reverse('tutorial:random-training'))
            request.session.pop('matrix_input')
        else:
            # this part works when there are no input
            matrix = Matrix.objects.last()
            if matrix is not None:
                context['matrix'] = matrix
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
    return render(request, 'training_for_random.html', context)'''


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


def state_update(request):
    matrix_id = request.session.get('matrix_id', None)
    qs = Matrix.objects.filter(id=matrix_id)
    if qs.count() == 1:
        matrix_obj = qs.first()
    state = request.POST.get('state')
    if state == 'beta1' and matrix_obj.controlled_state == '1':
        matrix_obj.controlled_state = '0'
        threshold(matrix_obj)
    elif state == 'beta2' and matrix_obj.controlled_state == '0':
        matrix_obj.controlled_state = '1'
        threshold(matrix_obj)
    matrix_obj.save()
    return redirect("tutorial:training_nr")


def row_update(request):
    matrix_id = request.session.get('matrix_id', None)
    qs = Matrix.objects.filter(id=matrix_id)
    if qs.count() == 1:
        matrix_obj = qs.first()
    row_id = request.POST.get('row_id')
    if row_id is not None:
        try:
            row_obj = Row.objects.get(id=row_id)
        except Row.DoesNotExist:
            return redirect("tutorial:training_nr")
        if row_obj in matrix_obj.matrix.all():
            row_obj.delete()
    else:
        row = Row(a0=float(request.POST.get('a0')),
                  a1=float(request.POST.get('a1')),
                  matrix=matrix_obj)
        row.save()
    threshold(matrix_obj)
    return redirect("tutorial:training_nr")


def threshold(matrix):
    if len(matrix.matrix.all()) != 0:
        a = []
        matrix_state = matrix.controlled_state
        for row in matrix.matrix.all():
            if matrix_state == '0':
                a.append(row.a0)
            else:
                a.append(row.a1)
        thrshld = round(random.uniform(min(a) - 1, max(a) + 1), 2)
        matrix.threshold = thrshld
        matrix.save()
    exclude_rows(matrix)
    answer_row(matrix)


def exclude_rows(matrix):
    matrix_state = matrix.controlled_state
    for row in matrix.matrix.all():
        if matrix_state == '0' and row.a0 >= matrix.threshold or matrix_state == '1' and row.a1 >= matrix.threshold:
            row.excluded = True
            row.save()
        else:
            row.excluded = False
            row.save()


def answer_row(matrix):
    matrix_state = matrix.controlled_state
    qs = matrix.matrix.all().filter(excluded=False)
    min_row = qs.first()
    for row in qs:
        if matrix_state == '0' and row.a1 < min_row.a1 or matrix_state == '1' and row.a0 < min_row.a0:
            min_row = row
    is_answer_qs = matrix.matrix.all().filter(is_answer=True)
    if len(is_answer_qs) != 0:
        former_is_answer = is_answer_qs.first()
        former_is_answer.is_answer = False
        former_is_answer.save()
    min_row.is_answer = True
    min_row.save()


def training_for_nrandom(request):
    context = {}
    matrix_id = request.session.get('matrix_id', None)
    qs = Matrix.objects.filter(id=matrix_id)
    if qs.count() == 1:
        matrix_obj = qs.first()
    else:
        matrix_obj = Matrix.objects.create()
        request.session['matrix_id'] = matrix_obj.id
    context['matrix'] = matrix_obj
    if len(matrix_obj.matrix.all()) < 3:
        context['warning'] = True
    '''if request.method == 'POST':
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
                context['color'] = 'color: red;'''
    return render(request, 'training_for_nrandom.html', context)
