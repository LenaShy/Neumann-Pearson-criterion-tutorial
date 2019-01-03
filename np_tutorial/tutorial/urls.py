from django.urls import path

from .views import \
    example_for_random, \
    example_for_nrandom, \
    training_for_nrandom, \
    get_data, \
    theory_for_random, \
    training_for_random

urlpatterns = [
    path('random/theory', theory_for_random, name='random-theory'),
    path('random/example', example_for_random, name='random-example'),
    path('random/training', training_for_random, name='random-training'),
    path('nrandom/', example_for_nrandom, name='nrandom'),
    path('nrandom/training/', training_for_nrandom, name='training_nr'),
    path('api/data/', get_data, name='api-data'),
]
