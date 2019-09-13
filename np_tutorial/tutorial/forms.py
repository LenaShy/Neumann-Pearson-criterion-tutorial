from django import forms
from django.core.exceptions import ValidationError


from .models import Matrix, Row


class MatrixForm(forms.ModelForm):

    class Meta:
        model = Matrix
        fields = ['id', ]
        exclude = ('name',)


class RowsForm(forms.Form):
    row1 = forms.BooleanField(required=False)
    row2 = forms.BooleanField(required=False)
    row3 = forms.BooleanField(required=False)
    case_losses = forms.FloatField()

    class Meta:
        model = Row
        fields = '__all__'



