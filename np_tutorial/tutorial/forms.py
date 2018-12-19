from django import forms
from django.core.exceptions import ValidationError


from .models import Matrix, MatrixRow


class MatrixRowForm(forms.ModelForm):
    class Meta:
        model = MatrixRow
        fields = ['a1', 'a2']


class MatrixForm(forms.ModelForm):
    CHOICES = (
        ('state1', "beta1"),
        ('state2', "beta2"),
    )

    class Meta:
        model = Matrix
        fields = ['a11', 'a12', 'a21', 'a22', 'a31', 'a32']

    state = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    '''def __init__(self, *args, **kwargs):
        super(MatrixForm, self).__init__(*args, **kwargs)
        rows = MatrixRow.objects.filter(
            matrix=self.instance
        )
        print(self.instance)
        print(rows)
        for i in range(len(rows)):
            field_name1 = 'row_%s1' % (i,)
            field_name2 = 'row_%s2' % (i,)
            self.fields[field_name1] = forms.DecimalField(required=False)
            self.fields[field_name2] = forms.DecimalField(required=False)
            try:
                self.initial[field_name1] = rows[i].a1
                self.initial[field_name2] = rows[i].a2
            except IndexError:
                self.initial[field_name1] = 0
                self.initial[field_name2] = 0

            # create an extra blank field
            field_name1 = 'row_%s1' % (i + 1,)
            field_name2 = 'row_%s2' % (i + 1,)
            self.fields[field_name1] = forms.DecimalField(required=False)
            self.fields[field_name2] = forms.DecimalField(required=False)'''


class ExcludeRowsForm(forms.Form):
    row1 = forms.BooleanField(required=False)
    row2 = forms.BooleanField(required=False)
    row3 = forms.BooleanField(required=False)


class RightAnswerForm(forms.Form):
    alpha_number = forms.IntegerField(widget=forms.NumberInput)
    alpha_number2 = forms.BooleanField()
    losses = forms.DecimalField()



