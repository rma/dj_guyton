import os
import os.path

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.forms.formsets import formset_factory, BaseFormSet

import guyton.queryforms
from guyton.models import Model, Experiment, OutputTask
from guyton.search import find, describe
from guyton.format import response
from guyton.tasks import generateOutput
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
        if action == 'Count Matches':
            matches = find(data)
            total = Experiment.objects.count()
            matched = str(matches.count())
            return render_to_response('search.html', {
                'matched': matched,
                'total': total,
                'param_formset': forms['params'],
                'var_formset': forms['vars'],
                'tag_formset': forms['tags'],
                'exp_form': forms['exp'],
                'out_form': forms['out'],
                'log_str': log_str,
            }, context_instance=RequestContext(request))
        elif action == 'Submit Query':
            matches = find(data)
            total = matches.count()
            fmt = lambda n, v, t: "%s %s %s" % (t, n, v)
            count = 1

            # Save the search criteria as the first file
            out_files.append(describe(data, comment_str=""))

            for experiment in matches:
                # Initial parameter values
                p_vals = experiment.paramvalue_set.filter(at_time__exact=0)
                # Changes to parameter values
                p_dels = experiment.paramvalue_set.filter(at_time__gt=0)

                exp_lines = []
                # Save the initial parameter values
                exp_lines.extend([fmt(p.parameter.name, p.value, p.at_time)
                                  for p in p_vals])
                # Save the parameter perturbations
                exp_lines.extend([fmt(p.parameter.name, p.value, p.at_time)
                                  for p in p_dels])

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
                    return 'experiment%d.txt' % (num - 1,)

            resp = compress_files(out_files, fname, 'results')

            return resp
            # task = OutputTask.create_new(data)
            # generateOutput(task.id)
            # return HttpResponseRedirect("tasks/" + task.sha256_id)
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

def show_task(request, task_hash):
    action = request.POST.get('form-submit')
    task = get_object_or_404(OutputTask, sha256_id=task_hash)
    if request.method == 'POST' and action == 'Delete Results':
        task.remove_task()
        return HttpResponseRedirect("/")
    else:
        result_url = "../../site_media/tasks/" + task_hash + ".tar.bz2"
        return render_to_response('task.html',
            {'task': task, 'url': result_url},
            context_instance=RequestContext(request))
