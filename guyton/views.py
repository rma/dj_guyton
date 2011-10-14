import os
import os.path

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.forms.formsets import formset_factory, BaseFormSet

import guyton.queryforms
from guyton.models import Individual
from guyton.search import find, describe
from guyton.compress import compress_files

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

def get_action(submitted, actions):
    for action in actions:
        if action in submitted:
            return action
    return ''

# Create your views here.
def index(request):
    log_str = ""

    forms = {
        'conds': (guyton.queryforms.ClinicalCondForm, True)
        }

    action = get_action(request.POST,
                        ['add-cond', 'del-cond', 'qry-cnt', 'qry-dl'])
    (forms, data, valid, modified) = validate_forms(request, action, forms)

    if request.method == 'POST' and valid and not modified:
        if action == 'qry-cnt':
            matches = find(data)
            total = Individual.objects.count()
            matched = str(matches.count())
            return render_to_response('search.html', {
                'matched': matched,
                'total': total,
                'cond_formset': forms['conds'],
                'log_str': log_str,
            }, context_instance=RequestContext(request))
        elif action == 'qry-dl':
            matches = find(data)
            total = matches.count()
            fmt = lambda name, value: "%s %s" % (name.lower(), value)
            count = 1

            # Save the search criteria as the first file
            out_files = []
            out_files.append(describe(data, comment_str=""))

            for individual in matches:
                exp_lines = []
                param_vals = individual.indivparam_set.all()

                # Save the initial parameter values
                exp_lines.extend([fmt(p.value.parameter.name, p.value.value)
                                  for p in param_vals])

                # Ensure the simulation runs for a minimum of 5 weeks
                exp_lines.append("")
                exp_lines.append("t= 50400.0")

                # Append this experiment to the list of files
                out_files.append(exp_lines)
                count += 1

            # Define the name of each file; the first one contains the search
            # critera, the others contain the parameter values for each
            # matching experiment.
            def fname(num):
                if num == 1:
                    return 'query.txt'
                else:
                    return 'individual%d.txt' % (num - 1,)

            resp = compress_files(out_files, fname, 'results')

            return resp
        else:
            err_msg = 'Invalid request: ' + action
            raise Http404(err_msg)

    return render_to_response('search.html', {
        'cond_formset': forms['conds'],
        'log_str': log_str,
    }, context_instance=RequestContext(request))
