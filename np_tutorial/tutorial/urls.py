from django.urls import path

from .views import example_for_random, example_for_nrandom, training_for_nrandom, get_data

urlpatterns = [
    path('random/', example_for_random, name='random'),
    path('nrandom/', example_for_nrandom, name='nrandom'),
    path('nrandom/training/', training_for_nrandom, name='training_nr'),
    path('api/data/', get_data, name='api-data'),
]
