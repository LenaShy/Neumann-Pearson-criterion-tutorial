from django import forms
from django.core.exceptions import ValidationError


from .models import Matrix, MatrixRow


class MatrixForm(forms.ModelForm):
    '''CHOICES = (
        ('\\(\\beta_{1}\\)', '\\(\\beta_{1}\\)'),
        ('\\(\\beta_{2}\\)', '\\(\\beta_{2}\\)'),
    )

    #state = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rows = MatrixRow.objects.filter(matrix=self.instance)
        for i in range(len(rows) + 1):
            field_name_0 = 'a_{}_0'.format(i)
            field_name_1 = 'a_{}_1'.format(i)
            self.fields[field_name_0] = forms.FloatField(required=False)
            self.fields[field_name_1] = forms.FloatField(required=False)
            try:
                self.initial[field_name_0] = rows[i].a_0
                self.initial[field_name_1] = rows[i].a_1
            except IndexError:
                self.initial[field_name_0] = 0.0
                self.initial[field_name_1] = 0.0

    def clean(self):
        rows = list()
        i = 0
        field_name_0 = 'a_{}_0'.format(i)
        field_name_1 = 'a_{}_1'.format(i)
        while self.cleaned_data[field_name_0] and self.cleaned_data[field_name_1]:
            a_0 = self.cleaned_data[field_name_0]
            a_1 = self.cleaned_data[field_name_1]
            rows.append([a_0, a_1])
            i += 1
            field_name_0 = 'a_{}_0'.format(i)
            field_name_1 = 'a_{}_1'.format(i)
        self.cleaned_data['rows'] = rows

    def save(self):
        matrix = self.instance

        matrix.a_0_set_all().delete()
        matrix.a_1_set_all().delete()
        for i in range(len(self.cleaned_data['rows'])):
            a_0 = self.cleaned_data['rows'][i][0]
            a_1 = self.cleaned_data['rows'][i][1]
            MatrixRow.objects.create(matrix=matrix, a_0=a_0, a_1=a_1)

    class Meta:
        model = Matrix
        exclude = ['name',
                   'state',
                   'threshold',
                   'exclude_alpha1',
                   'exclude_alpha2',
                   'exclude_alpha3',
                   'losses',
                   'answer_nrand',
                   'answer_rand']


class RowsForm(forms.Form):
    row1 = forms.BooleanField(required=False)
    row2 = forms.BooleanField(required=False)
    row3 = forms.BooleanField(required=False)
    case_losses = forms.FloatField()



