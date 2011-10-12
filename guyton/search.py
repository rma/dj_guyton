import time

from guyton.models import Individual

def find(search_data, just_sql=False):
    param_data = search_data['params']
    var_data = search_data['vars']

    indivs = Individual.objects.all()

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
                indivvar__value__value__ltt=v['value'])
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

def describe(search_data, comment_str='# '):
    param_data = search_data['params']
    var_data = search_data['vars']

    constraints = ['Query submitted at %s' % (time.strftime('%c'),), '']
    constraints.append('Constraints:')

    for p in param_data:
        if p['param'] is None:
            continue
        pname = p['param'].name
        pvalue = p['value']
        pop = describe_op(p['operator'])

        constr = "\tPARAM\t%s\t%s\t%s" % (pname, pop, pvalue)
        constraints.append(constr)

    for v in var_data:
        if v['var'] is None:
            continue
        vname = v['var'].name
        vvalue = v['value']
        vop = describe_op(v['operator'])

        constr = "\tVAR\t%s\t%s\t%s" % (vname, vop, vvalue)
        constraints.append(constr)

    comment_line = lambda line: comment_str + line

    return map(comment_line, constraints)
