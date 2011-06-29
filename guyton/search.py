import time

from guyton.models import Experiment, Parameter, Variable, Tag, Model

def find(search_data, just_sql=False):
    param_data = search_data['params']
    var_data = search_data['vars']
    tag_data = search_data['tags']
    exp_data = search_data['exp']
    matches = Experiment.objects.all()

    for p in param_data:
        if p['param'] is None:
            continue
        if p['operator'] == 'EQ':
            if int(p['when']) == 0:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__exact=p['value'])
            elif int(p['when']) == 1:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__exact=p['value'],
                    paramvalue__at_time__exact=0)
            elif int(p['when']) == 2:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__exact=p['value'],
                    paramvalue__at_time__gt=0)
            else:
                pass
        elif p['operator'] == 'NE':
            # Bug #14645
            # http://code.djangoproject.com/ticket/14645
            pass
            # matches = matches.extra(where=['NOT ("par_value"."parameter" = %s '
            #     'AND "par_value"."value" = %s)'],
            #     params=[p['param'].id, p['value']])
        elif p['operator'] == 'LT':
            if int(p['when']) == 0:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__lt=p['value'])
            elif int(p['when']) == 1:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__lt=p['value'],
                    paramvalue__at_time__exact=0)
            elif int(p['when']) == 2:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__lt=p['value'],
                    paramvalue__at_time__gt=0)
            else:
                pass
        elif p['operator'] == 'LE':
            if int(p['when']) == 0:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__lte=p['value'])
            elif int(p['when']) == 1:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__lte=p['value'],
                    paramvalue__at_time__exact=0)
            elif int(p['when']) == 2:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__lte=p['value'],
                    paramvalue__at_time__gt=0)
            else:
                pass
        elif p['operator'] == 'GT':
            if int(p['when']) == 0:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__gt=p['value'])
            elif int(p['when']) == 1:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__gt=p['value'],
                    paramvalue__at_time__exact=0)
            elif int(p['when']) == 2:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__gt=p['value'],
                    paramvalue__at_time__gt=0)
            else:
                pass
        elif p['operator'] == 'GE':
            if int(p['when']) == 0:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__gte=p['value'])
            elif int(p['when']) == 1:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__gte=p['value'],
                    paramvalue__at_time__exact=0)
            elif int(p['when']) == 2:
                matches = matches.filter(
                    paramvalue__parameter__exact=p['param'].id,
                    paramvalue__value__gte=p['value'],
                    paramvalue__at_time__gt=0)
            else:
                pass
        else:
            pass

    for v in var_data:
        if v['var'] is None:
            continue
        if v['operator'] == 'EQ':
            if int(v['when']) == 0:
                matches = matches.filter(
                    varvalue__variable__exact=v['var'].id,
                    varvalue__value__exact=v['value'])
            else:
                matches = matches.filter(
                    varvalue__variable__exact=v['var'].id,
                    varvalue__value__exact=v['value'],
                    varvalue__why_now__exact=v['when'])
        elif v['operator'] == 'NE':
            # Bug #14645
            # http://code.djangoproject.com/ticket/14645
            pass
            # matches = matches.extra(where=['NOT ("var_value"."variable" = %s '
            #     'AND "var_value"."value" = %s)'],
            #     params=[(v['var'].id, v['value'])])
        elif v['operator'] == 'LT':
            if int(v['when']) == 0:
                matches = matches.filter(
                    varvalue__variable__exact=v['var'].id,
                    varvalue__value__lt=v['value'])
            else:
                matches = matches.filter(
                    varvalue__variable__exact=v['var'].id,
                    varvalue__value__lt=v['value'],
                    varvalue__why_now__exact=v['when'])
        elif v['operator'] == 'LE':
            if int(v['when']) == 0:
                matches = matches.filter(
                    varvalue__variable__exact=v['var'].id,
                    varvalue__value__lte=v['value'])
            else:
                matches = matches.filter(
                    varvalue__variable__exact=v['var'].id,
                    varvalue__value__lte=v['value'],
                    varvalue__why_now__exact=v['when'])
        elif v['operator'] == 'GT':
            if int(v['when']) == 0:
                matches = matches.filter(
                    varvalue__variable__exact=v['var'].id,
                    varvalue__value__gt=v['value'])
            else:
                matches = matches.filter(
                    varvalue__variable__exact=v['var'].id,
                    varvalue__value__gt=v['value'],
                    varvalue__why_now__exact=v['when'])
        elif v['operator'] == 'GE':
            if int(v['when']) == 0:
                matches = matches.filter(
                    varvalue__variable__exact=v['var'].id,
                    varvalue__value__gte=v['value'])
            else:
                matches = matches.filter(
                    varvalue__variable__exact=v['var'].id,
                    varvalue__value__gte=v['value'],
                    varvalue__why_now__exact=v['when'])

    for t in tag_data:
        if t['tag'] is not None:
            matches = matches.filter(taggedwith__tag__exact=t['tag'])

    which_model = exp_data['model']
    if which_model is not None:
        matches = matches.filter(model__exact=which_model)
    which_user = exp_data['user']
    if which_user is not None and len(which_user) > 0:
        matches = matches.filter(by_user__exact=which_user)
    which_host = exp_data['host']
    if which_host is not None and len(which_host) > 0:
        matches = matches.filter(on_host__exact=which_host)

    if just_sql:
        return str(matches.query)
    else:
        return matches.distinct()

def describe(search_data, comment_str='# '):
    param_data = search_data['params']
    var_data = search_data['vars']
    tag_data = search_data['tags']
    exp_data = search_data['exp']
    matches = Experiment.objects.all()

    which_model = exp_data['model']
    which_user = exp_data['user']
    which_host = exp_data['host']

    constraints = ['Query submitted at %s' % (time.strftime('%c'),), '']
    constraints.append('Constraints:')

    for p in param_data:
        if p['param'] is None:
            continue
        pname = p['param'].name
        pvalue = p['value']
        pop = p['operator']
        if int(p['when']) == 0:
            pwhen = "Any Time"
        elif int(p['when']) == 1:
            pwhen = "Pre-perturbation"
        elif int(p['when']) == 2:
            pwhen = "Post-perturbation"
        else:
            pass

        constr = "\tPARAM\t%s\t%s\t%s\tat\t%s" % (pname, pop, pvalue, pwhen)
        constraints.append(constr)

    for v in var_data:
        if v['var'] is None:
            continue
        vname = v['var'].name
        vvalue = v['value']
        vop = v['operator']
        if int(v['when']) == 0:
            vwhen = "Any Time"
        elif int(v['when']) == 1:
            vwhen = "Pre-perturbation"
        elif int(v['when']) == 2:
            vwhen = "1 Minute"
        elif int(v['when']) == 3:
            vwhen = "1 Hour"
        elif int(v['when']) == 4:
            vwhen = "1 Day"
        elif int(v['when']) == 5:
            vwhen = "1 Week"
        elif int(v['when']) == 6:
            vwhen = "4 Weeks"
        else:
            pass

        constr = "\tVAR\t%s\t%s\t%s\tat\t%s" % (vname, vop, vvalue, vwhen)
        constraints.append(constr)

    for t in tag_data:
        if t['tag'] is not None:
            tname = t['tag'].name
            constr_str = "TAG\t%s" % (tname,)
            constraints.append(constr_str)

    which_model = exp_data['model']
    if which_model is not None:
        constraints.append("\tMODEL\t%s" % (which_model.name,))

    which_user = exp_data['user']
    if which_user is not None and len(which_user) > 0:
        constraints.append("\tUSER\t%s" % (which_user,))

    which_host = exp_data['host']
    if which_host is not None and len(which_host) > 0:
        constraints.append("\tHOST\t%s" % (which_host,))

    comment_line = lambda line: comment_str + line

    return map(comment_line, constraints)
