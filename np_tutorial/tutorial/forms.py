from django import forms


class Matrix(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Matrix, self).__init__(*args, **kwargs)
        for i in range(int(args[0]/2)):
            self.fields['a' + str(i) + '1'] = forms.DecimalField()
            self.fields['a' + str(i) + '2'] = forms.DecimalField()
