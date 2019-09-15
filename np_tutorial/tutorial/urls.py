from django.urls import path

from .views import training_for_nrandom, \
    get_data, \
    theory_for_random, \
    example_for_nrandom,\
    matrix_home, \
    row_update
    #example_for_random,
    #training_for_random

urlpatterns = [
    path('random/theory', theory_for_random, name='random-theory'),
    #path('random/example', example_for_random, name='random-example'),
    #path('random/training', training_for_random, name='random-training'),
    path('nrandom/', example_for_nrandom, name='nrandom'),
    path('nrandom/training/', training_for_nrandom, name='training_nr'),
    path('api/data/', get_data, name='api-data'),
    path('nrandom/training/matrix_home', matrix_home, name='matrix-home'),
    path('nrandom/training/row_update', row_update, name='row-update'),
]
