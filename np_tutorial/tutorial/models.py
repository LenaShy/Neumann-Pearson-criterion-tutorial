from django.db import models

from picklefield.fields import PickledObjectField


class Matrix(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, default='\\(\\beta_{1}\\)')
    threshold = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    exclude_alpha1 = models.BooleanField(default=False)
    exclude_alpha2 = models.BooleanField(default=False)
    exclude_alpha3 = models.BooleanField(default=False)
    losses = models.FloatField(default=0)
    answer_nrand = PickledObjectField(default=list)
    answer_rand = PickledObjectField(default=list)


class MatrixRow(models.Model):
    a_0 = models.FloatField()
    a_1 = models.FloatField()
    matrix = models.ForeignKey(Matrix, related_name='matrix', on_delete=models.CASCADE)




