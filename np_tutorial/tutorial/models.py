from django.db import models
from django.core.validators import DecimalValidator

from picklefield.fields import PickledObjectField


class Matrix(models.Model):
    STATE_CHOICES = (
        ('0', 'beta_{1}'),
        ('1', 'beta_{2}'),
    )
    name = models.CharField(max_length=20, blank=True, null=True)
    controlled_state = models.CharField(max_length=10, choices=STATE_CHOICES)
    threshold = models.FloatField(default=0)

    def __str__(self):
        return str(self.id)


class Row(models.Model):
    a0 = models.FloatField()
    a1 = models.FloatField()
    matrix = models.ForeignKey(Matrix, related_name='matrix', on_delete=models.CASCADE)
    excluded = models.BooleanField(default=False)
    is_answer = models.BooleanField(default=False)
    message = models.CharField(max_length=20, default='')







