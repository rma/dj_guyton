from guyton.models import Experiment

def find(param_data, var_data, tag_data, exp_data):
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

    matches = matches.distinct()
    return matches
