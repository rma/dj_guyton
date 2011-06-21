from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.formsets import formset_factory, BaseFormSet

import guyton.queryforms
from guyton.models import Model, Experiment
from guyton.search import find
from guyton.format import response

def validate_form(form, action, modify_form=False):
    if form.is_valid():
        form_data = form.cleaned_data

        if isinstance(form, BaseFormSet):
            if action == form.form.ADD_ACTION:
                modify_form = True
                form_data.append(form.form.DEFAULT_DATA)
            elif action == form.form.DEL_ACTION:
                modify_form = True
                del_fn = lambda subform: not subform[form.form.DEL_FIELD]
                form_data = filter(del_fn, form_data)
                # Ensure there is always an empty condition
                if len(form_data) == 0:
                    form_data = [form.form.DEFAULT_DATA]

        return (form_data, modify_form)
    else:
        return (None, False)

def validate_forms(request, action, forms):
    valid_forms = True
    modify_form = False
    new_forms = {}
    new_data = {}

    for prefix in forms.iterkeys():
        (form_class, as_formset) = forms[prefix]
        if as_formset:
            factory = formset_factory(form_class, extra=0)
        else:
            factory = form_class

        if request.method == 'POST':
            form = factory(request.POST, prefix=prefix)
            (form_data, modify_form) = validate_form(form, action, modify_form)

            if form_data is None:
                valid_forms = False
            elif as_formset:
                form = factory(initial=form_data, prefix=prefix)
        else:
            if as_formset:
                form_data = [form_class.DEFAULT_DATA]
                form = factory(initial=form_data, prefix=prefix)
            else:
                form_data = None
                form = factory(prefix=prefix)

        new_forms[prefix] = form
        new_data[prefix] = form_data

    return (new_forms, new_data, valid_forms, modify_form)

# Create your views here.
def index(request):
    log_str = ""

    forms = {
        'params': (guyton.queryforms.ParamCondForm, True),
        'vars': (guyton.queryforms.VarCondForm, True),
        'tags': (guyton.queryforms.TagCondForm, True),
        'exp': (guyton.queryforms.ExpCondForm, False),
        'out': (guyton.queryforms.OutputChoiceForm, False),
        }

    action = request.POST.get('form-submit')
    (forms, data, valid, modified) = validate_forms(request, action, forms)

    if request.method == 'POST' and valid and not modified:
        if action == 'Submit':
            matches = find(data['params'], data['vars'],
                           data['tags'], data['exp'])
            return response(matches, data['out'])
        else:
            err_msg = 'Invalid request: ' + action
            raise Http404(err_msg)

    return render_to_response('search.html', {
        'param_formset': forms['params'],
        'var_formset': forms['vars'],
        'tag_formset': forms['tags'],
        'exp_form': forms['exp'],
        'out_form': forms['out'],
        'log_str': log_str,
    }, context_instance=RequestContext(request))

def list_details(request):
    model_list = Model.objects.all().order_by('name')
    sort_field = lambda f: Experiment.objects.values(f).distinct().order_by(f)
    user_list = sort_field('by_user')
    host_list = sort_field('on_host')

    return render_to_response('detail_list.html', {
        'model_list': model_list,
        'user_list': user_list,
        'host_list': host_list,
    }, context_instance=RequestContext(request))