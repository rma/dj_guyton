import cStringIO
import sys
import tarfile
import time
import zipfile

from django.http import HttpResponse

# Accepts a list of lines (ie, a list that contains lists of strings), a
# function that determines the name for each set of lines, and the output
# file name (minus the extension). The result is a HttpResponse objects that
# returns a .zip file containing all of the files.
def compress_files(list_of_lines, file_name_fn, result_file):
    store = cStringIO.StringIO()
    fzip = zipfile.ZipFile(store , "w" , zipfile.ZIP_DEFLATED)

    count = 1
    for lines in list_of_lines:
        file_data = "\n".join(lines)
        file_name = file_name_fn(count)
        fzip.writestr(file_name, file_data)
        count += 1

    fzip.close()
    zip_data = store.getvalue()
    store.close()

    resp = HttpResponse(zip_data, mimetype="application/zip")
    attach_str = 'attachment; filename=%s' % (result_file + '.zip',)
    resp['Content-Disposition'] = attach_str

    return resp
