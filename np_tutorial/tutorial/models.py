from django.db import models

from picklefield.fields import PickledObjectField


class Matrix(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    a11 = models.FloatField(default=0)
    a12 = models.FloatField(default=0)
    a21 = models.FloatField(default=0)
    a22 = models.FloatField(default=0)
    a31 = models.FloatField(default=0)
    a32 = models.FloatField(default=0)
    state = models.CharField(max_length=20, default='\\(\\beta_{1}\\)')
    threshold = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    exclude_alpha1 = models.BooleanField(default=False)
    exclude_alpha2 = models.BooleanField(default=False)
    exclude_alpha3 = models.BooleanField(default=False)
    losses = models.FloatField(default=0)
    answers = PickledObjectField(default=list)


class MatrixRow(models.Model):
    a1 = models.DecimalField(max_digits=4, decimal_places=2)
    a2 = models.DecimalField(max_digits=4, decimal_places=2)
    matrix = models.ForeignKey(Matrix, related_name='matrix', on_delete=models.CASCADE)


