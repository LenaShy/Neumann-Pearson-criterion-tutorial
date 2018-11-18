from django.urls import path

from .views import theory_for_random

urlpatterns = [
    path('random/', theory_for_random, name='random'),
]
