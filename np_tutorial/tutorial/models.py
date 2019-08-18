from django.db import models

from picklefield.fields import PickledObjectField


class Matrix(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    decision_amount = models.IntegerField(default=0)
    state = models.CharField(max_length=20, default='\\(\\beta_{1}\\)')
    threshold = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    exclude_alpha1 = models.BooleanField(default=False)
    exclude_alpha2 = models.BooleanField(default=False)
    exclude_alpha3 = models.BooleanField(default=False)
    losses = models.FloatField(default=0)
    answer_nrand = PickledObjectField(default=list)
    answer_rand = PickledObjectField(default=list)

    def __init__(self, n=5):
        self.decision_amount = n
        for i in range(self.decision_amount):
            field_name1 = 'a{0}1'.format(i)
            field_name2 = 'a{0}2'.format(i)
            self.__dict__[field_name1] = models.FloatField(default=0)
            self.__dict__[field_name2] = models.FloatField(default=0)


class MatrixRow(models.Model):
    a1 = models.DecimalField(max_digits=4, decimal_places=2)
    a2 = models.DecimalField(max_digits=4, decimal_places=2)
    matrix = models.ForeignKey(Matrix, related_name='matrix', on_delete=models.CASCADE)




