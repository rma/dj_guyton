from django import forms
from django.forms.formsets import formset_factory
from django.core import validators

from models import Parameter, Variable, Model

op_choices = (('EQ', '='), ('LT', '<'),
              ('LE', '<='), ('GT', '>'), ('GE', '>='))

class ParamCondForm(forms.Form):
    ADD_ACTION = 'Add Parameter'
    DEL_ACTION = 'Remove Parameters'
    DEL_FIELD = 'sel'
    DEFAULT_DATA = {'param': None, 'operator': u'EQ', 'value': None,
                    'sel': False}

    param = forms.ModelChoiceField(Parameter.objects.order_by('name'),
                                   label='Parameter', required=False)
    operator = forms.ChoiceField(op_choices, label='Relationship',
                                 required=False)
    value = forms.DecimalField(label='Value', required=False)
    sel = forms.BooleanField(label='Remove', required=False)

class VarCondForm(forms.Form):
    ADD_ACTION = 'Add Variable'
    DEL_ACTION = 'Remove Variables'
    DEL_FIELD = 'sel'
    DEFAULT_DATA = {'var': None, 'operator': u'EQ', 'value': None,
                    'sel': False}

    var = forms.ModelChoiceField(Variable.objects.order_by('name'),
                                    label='Variable', required=False)
    operator = forms.ChoiceField(op_choices, label='Relationship',
                                    required=False)
    value = forms.DecimalField(label='Value', required=False)
    sel = forms.BooleanField(label='Remove', required=False)

class ModelForm(forms.Form):
    model = forms.ModelChoiceField(Model.objects.order_by('name'),
                                      label='Model', required=True,
                                      initial=Model.objects.all()[0].id)
