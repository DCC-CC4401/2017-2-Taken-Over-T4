from django.forms import forms


class graphForm(forms.Form):
    choices = choices = [(0, 'Última semana'),
                         (1, 'Último mes'),
                         (2, 'Último trimestre'),
                         (3, 'Últimos seis meses'),
                         (4, 'Último año')]
    action = forms.ChoiceField(choices=choices,
                               widget=forms.Select(attrs={'onchange': 'graphForm.submit();'}))

