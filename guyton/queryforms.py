from django import forms
from django.forms.formsets import formset_factory
from django.core import validators

from models import Parameter, Variable, Tag, Model

op_choices = (('EQ', '='), ('LT', '<'),
              ('LE', '<='), ('GT', '>'), ('GE', '>='))

# TODO -- derive this list from TIME_DETAIL
time_choices = ((0, 'Any Time'), (1, 'Pre-perturbation'),
                (2, '1 Minute'), (3, '1 Hour'), (4, '1 Day'),
                (5, '1 Week'), (6, '4 Weeks'),)

param_times = ((0, 'Any Time'), (1, 'Pre-perturbation'),
               (2, 'Post-perturbation'))

class ParamCondForm(forms.Form):
    ADD_ACTION = 'Add Parameter'
    DEL_ACTION = 'Remove Parameters'
    DEL_FIELD = 'sel'
    DEFAULT_DATA = {'param': None, 'operator': u'EQ', 'value': None,
                    'when': u'0', 'sel': False}

    param = forms.ModelChoiceField(Parameter.objects.order_by('name'),
                                   label='Parameter', required=False)
    operator = forms.ChoiceField(op_choices, label='Relationship',
                                 required=False)
    value = forms.DecimalField(label='Value', required=False)
    when = forms.ChoiceField(param_times, label='At Time', required=False)
    sel = forms.BooleanField(label='Remove', required=False)

class VarCondForm(forms.Form):
    ADD_ACTION = 'Add Variable'
    DEL_ACTION = 'Remove Variables'
    DEL_FIELD = 'sel'
    DEFAULT_DATA = {'var': None, 'operator': u'EQ', 'value': None,
                    'when': u'0', 'sel': False}

    var = forms.ModelChoiceField(Variable.objects.order_by('name'),
                                    label='Variable', required=False)
    operator = forms.ChoiceField(op_choices, label='Relationship',
                                    required=False)
    value = forms.DecimalField(label='Value', required=False)
    when = forms.ChoiceField(time_choices, label='At Time', required=False)
    #when = forms.ModelChoiceField(TimeDetail.objects.order_by('id'),
    #                              label='At Time', required=False)
    sel = forms.BooleanField(label='Remove', required=False)

class TagCondForm(forms.Form):
    ADD_ACTION = 'Add Tag'
    DEL_ACTION = 'Remove Tags'
    DEL_FIELD = 'sel'
    DEFAULT_DATA = {'tag': None, 'sel': False}

    tag = forms.ModelChoiceField(Tag.objects.order_by('name'),
                                 label='Tags', required=False)
    sel = forms.BooleanField(label='Remove', required=False)

class ExpCondForm(forms.Form):
    model = forms.ModelChoiceField(Model.objects.order_by('name'),
                                      label='Model', required=True)
    user = forms.CharField(label='User', validators=[], required=False)
    host = forms.CharField(label='Host', validators=[], required=False)

out_choices = (('I', 'Initial parameters'), ('P', 'All parameters'),
               ('S', 'Steady-state variables'), ('A', 'All details'),
              )

class OutputChoiceForm(forms.Form):
    data = forms.ChoiceField(out_choices, label='Output', required=True)
