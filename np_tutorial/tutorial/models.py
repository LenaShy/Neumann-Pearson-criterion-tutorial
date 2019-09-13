from django.db import models

from picklefield.fields import PickledObjectField


class Matrix(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Row(models.Model):
    a0 = models.FloatField()
    a1 = models.FloatField()
    matrix = models.ForeignKey(Matrix, related_name='matrix', on_delete=models.CASCADE)






