from django.http import HttpResponse
import csv

def response(matches, out_data):
    chosen_data = out_data['data']
    if chosen_data == 'I':
        out_str = 'Initial parameters'
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=results.csv'
        writer = csv.writer(response)
        # TODO -- assume all experiments are from the same model
        # and therefore have the same parameters
        # TODO -- order by model and treat each group separately!
        names = [v[0] for v in matches[0].paramvalue_set.filter(at_time__exact=0).order_by('parameter').values_list('parameter__name')]
        writer.writerow(names)
        for expID in matches:
            params = expID.paramvalue_set.all().order_by('parameter')
            values = [pval.value for pval in params]
            writer.writerow(values)
        return response
    elif chosen_data == 'P':
        # For each expID:
        #   Select (and order by) distinct paramvalue__at_time
        #   Then, for each at_time, print time, [name, value]+
        out_str = 'All parameters'
    elif chosen_data == 'S':
        out_str = 'Steady-state variables'
        # As per 'Initial parameters', but have to sort out which
        # at_time ... at_time__max is the key
    elif chosen_data == 'A':
        # Hmm ... need to sort this out ... all params and all
        # state snapshots for each experiment
        out_str = 'All details'

    return HttpResponse("Matches: " + str(len(matches)) + "<p>Returning: " + out_str + "<p>" + str(matches.query))
