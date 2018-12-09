from django.urls import path

from .views import theory_for_random, example_for_nrandom, training_for_nrandom

urlpatterns = [
    path('random/', theory_for_random, name='random'),
    path('nrandom/', example_for_nrandom, name='nrandom'),
    path('nrandom/training/', training_for_nrandom, name='training_nr')
]
