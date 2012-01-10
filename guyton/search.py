import time

from guyton.models import Individual, Variable
from guyton.queryforms import clin_choices

def find(search_data, just_sql=False):
    cond_data = search_data['conds']

    indiv_params = IndivParam.objects.all()
    indiv_vars = IndivVar.objects.all()

    for c in cond_data:
        if c['cond'] is None:
            continue

        # Lookup the ID of the named variable
        cond_var = Variable.objects.get(name__exact=c['cond'])

        if c['operator'] == 'EQ':
            indiv_vars = indiv_vars.filter(
                variable__exact=cond_var,
                value__exact=c['value'])
        elif c['operator'] == 'NE':
            # Bug #14645
            # http://code.djangoproject.com/ticket/14645
            pass
        elif c['operator'] == 'LT':
            indiv_vars = indiv_vars.filter(
                variable__exact=cond_var,
                value__lt=c['value'])
        elif c['operator'] == 'LE':
            indiv_vars = indiv_vars.filter(
                variable__exact=cond_var,
                value__lte=c['value'])
        elif c['operator'] == 'GT':
            indiv_vars = indiv_vars.filter(
                variable__exact=cond_var,
                value__gt=c['value'])
        elif c['operator'] == 'GE':
            indiv_vars = indiv_vars.filter(
                variable__exact=cond_var,
                value__ge=c['value'])

    #
    # The order_by() call is required before the distinct() call, as per:
    #   https://docs.djangoproject.com/en/1.3/ref/models/querysets/
    #
    indiv_vars = indiv_vars.order_by('individual').distinct('individual')

    if just_sql:
        return str(indiv_vars.query)
    else:
        indiv_ids = indiv_vars.values_list('individual', flat=True)
        indivs = Individual.objects.filter(id__in=indiv_ids)
        return indivs

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
