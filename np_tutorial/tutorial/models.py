from django.db import models


class Matrix(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    a11 = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    a12 = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    a21 = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    a22 = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    a31 = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    a32 = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    state = models.CharField(max_length=20, default='beta1')
    threshold = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    exclude_alpha1 = models.BooleanField(default=False)
    exclude_alpha2 = models.BooleanField(default=False)
    exclude_alpha3 = models.BooleanField(default=False)



class MatrixRow(models.Model):
    a1 = models.DecimalField(max_digits=4, decimal_places=2)
    a2 = models.DecimalField(max_digits=4, decimal_places=2)
    matrix = models.ForeignKey(Matrix, related_name='matrix', on_delete=models.CASCADE)


