import time

from guyton.models import Individual, Variable
from guyton.queryforms import clin_choices

def find(search_data, just_sql=False):
    cond_data = search_data['conds']

    indivs = Individual.objects.all()

    for c in cond_data:
        if c['cond'] is None:
            continue
        # Lookup the ID of the named variable
        cond_var = Variable.objects.get(name__exact=c['cond'])
        if c['operator'] == 'EQ':
            indivs = indivs.filter(
                indivvar__value__variable__exact=cond_var,
                indivvar__value__value__exact=c['value'])
        elif c['operator'] == 'NE':
            # Bug #14645
            # http://code.djangoproject.com/ticket/14645
            pass
        elif c['operator'] == 'LT':
            indivs = indivs.filter(
                indivvar__value__variable__exact=cond_var,
                indivvar__value__value__lt=c['value'])
        elif c['operator'] == 'LE':
            indivs = indivs.filter(
                indivvar__value__variable__exact=cond_var,
                indivvar__value__value__lte=c['value'])
        elif c['operator'] == 'GT':
            indivs = indivs.filter(
                indivvar__value__variable__exact=cond_var,
                indivvar__value__value__gt=c['value'])
        elif c['operator'] == 'GE':
            indivs = indivs.filter(
                indivvar__value__variable__exact=cond_var,
                indivvar__value__value__ge=c['value'])

    if just_sql:
        return str(indivs.query)
    else:
        return indivs.distinct()

    for p in param_data:
        if p['param'] is None:
            continue
        if p['operator'] == 'EQ':
            indivs = indivs.filter(
                indivparam__value__parameter__exact=p['param'].id,
                indivparam__value__value__exact=p['value'])
        elif p['operator'] == 'NE':
            # Bug #14645
            # http://code.djangoproject.com/ticket/14645
            pass
            # matches = matches.extra(where=['NOT ("par_value"."parameter" = %s '
            #     'AND "par_value"."value" = %s)'],
            #     params=[p['param'].id, p['value']])
        elif p['operator'] == 'LT':
            indivs = indivs.filter(
                indivparam__value__parameter__exact=p['param'].id,
                indivparam__value__value__lt=p['value'])
        elif p['operator'] == 'LE':
            indivs = indivs.filter(
                indivparam__value__parameter__exact=p['param'].id,
                indivparam__value__value__lte=p['value'])
        elif p['operator'] == 'GT':
            indivs = indivs.filter(
                indivparam__value__parameter__exact=p['param'].id,
                indivparam__value__value__gt=p['value'])
        elif p['operator'] == 'GE':
            indivs = indivs.filter(
                indivparam__value__parameter__exact=p['param'].id,
                indivparam__value__value__gte=p['value'])
        else:
            pass

    for v in var_data:
        if v['var'] is None:
            continue
        if v['operator'] == 'EQ':
            indivs = indivs.filter(
                indivvar__value__variable__exact=v['var'].id,
                indivvar__value__value__exact=v['value'])
        elif v['operator'] == 'NE':
            # Bug #14645
            # http://code.djangoproject.com/ticket/14645
            pass
            # matches = matches.extra(where=['NOT ("var_value"."variable" = %s '
            #     'AND "var_value"."value" = %s)'],
            #     params=[(v['var'].id, v['value'])])
        elif v['operator'] == 'LT':
            indivs = indivs.filter(
                indivvar__value__variable__exact=v['var'].id,
                indivvar__value__value__lt=v['value'])
        elif v['operator'] == 'LE':
            indivs = indivs.filter(
                indivvar__value__variable__exact=v['var'].id,
                indivvar__value__value__lte=v['value'])
        elif v['operator'] == 'GT':
            indivs = indivs.filter(
                indivvar__value__variable__exact=v['var'].id,
                indivvar__value__value__gt=v['value'])
        elif v['operator'] == 'GE':
            indivs = indivs.filter(
                indivvar__value__variable__exact=v['var'].id,
                indivvar__value__value__ge=v['value'])

    if just_sql:
        return str(indivs.query)
    else:
        return indivs.distinct()

def describe_op(op):
    if op == 'EQ':
        return '=='
    elif op == 'NE':
        return '!='
    elif op == 'LT':
        return '<'
    elif op == 'LE':
        return '<='
    elif op == 'GT':
        return '>'
    elif op == 'GE':
        return '>='
    else:
        return "??"

def describe_name(name):
    for (cname, cdesc) in clin_choices:
        if cname == name:
            return cdesc
    for (group, choices) in clin_choices:
        for (cname, cdesc) in choices:
            if cname == name:
                return cdesc
    return None

def describe(search_data, comment_str='# '):
    cond_data = search_data['conds']

    conditions = ['Query submitted at %s' % (time.strftime('%c'),), '']

    for c in cond_data:
        cname = describe_name(c['cond'])
        print c['cond'], ' --> ', cname
        if cname is None:
            continue
        cvalue = c['value']
        cop = describe_op(c['operator'])

        cond_desc = "%s\t%s\t%s" % (cname, cop, cvalue)
        conditions.append(cond_desc)

    comment_line = lambda line: comment_str + line

    return map(comment_line, conditions)
