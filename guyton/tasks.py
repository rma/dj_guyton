import cPickle
import os.path
import shutil
import subprocess
import tarfile
import tempfile

from celery.task import Task, task
from celery.registry import tasks
from celery.task.control import revoke

import settings

from guyton.models import OutputTask
from guyton.search import find

@task(ignore_result=True)
def generateOutput(output_task_id):
    task = OutputTask.objects.get(id=output_task_id)
    search_data = cPickle.loads(task.search_form.encode('utf-8'))
    experiments = find(search_data)

    return_data = search_data['out']['data']
    if return_data == 'I':
        pass
    elif return_data == 'P':
        pass
    elif return_data == 'S':
        pass
    elif return_data == 'A':
        pass
    else:
        task.is_finished = True
        task.save()
        return

    # TODO -- write the results of the search

    # create the temporary directory to store the script results
    tmp_dir = tempfile.mkdtemp()
    out_dir = os.path.join(os.path.dirname(__file__), 'site_media', 'tasks')

    # TODO -- run the script
    script_name = 'test.sh'
    script = os.path.join(settings.TASK_SCRIPT_DIR, script_name)
    subprocess.call(script, shell=True, cwd=tmp_dir)

    # collect all files and zip them
    result_files = os.listdir(tmp_dir)
    tmp_tar = tempfile.NamedTemporaryFile(delete=False)
    t = tarfile.open(fileobj=tmp_tar, mode='w:bz2')
    for f in result_files:
        filename = os.path.join(tmp_dir, f)
        t.add(filename, arcname=f)
    t.close()
    tmp_tar.close()

    # move the results to a django-accessible directory
    shutil.move(tmp_tar.name, task.output_abs_path())

    # delete all files (and temp_dir)
    shutil.rmtree(tmp_dir)

    # mark the task as finished
    task.is_finished = True
    task.save()

tasks.register(generateOutput)
