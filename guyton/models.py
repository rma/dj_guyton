# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

import cPickle
import datetime
import hashlib
import os

from django.db import models

class OutputTask(models.Model):
    sha256_id = models.CharField(max_length=70)
    search_form = models.TextField()
    is_finished = models.BooleanField()
    output_file = models.CharField(max_length=96)

    @staticmethod
    def create_new(search_data):
        search_str = cPickle.dumps(search_data)
        hash = hashlib.sha256()
        hash.update(str(datetime.datetime.utcnow()))
        hash.update(search_str)
        sha256_id = hash.hexdigest()
        output_file = sha256_id + '.tar.bz2'
        task = OutputTask.objects.create(sha256_id=sha256_id,
            search_form=search_str, is_finished=False, output_file=output_file)
        return task

    def output_abs_path(self):
        return os.path.join(os.path.dirname(__file__),
            'site_media', 'tasks', self.output_file)

    def remove_task(self):
        os.remove(self.output_abs_path())
        self.delete()

class Model(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    reference = models.TextField()
    class Meta:
        db_table = u'model'
    def __unicode__(self):
        return self.name

class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    class Meta:
        db_table = u'tag'
    def __unicode__(self):
        return self.name

class Parameter(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    units = models.TextField()
    description = models.TextField()
    min_val = models.FloatField()
    max_val = models.FloatField()
    default_val = models.FloatField()
    class Meta:
        db_table = u'parameter'
    def __unicode__(self):
        return self.name

class Variable(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    units = models.TextField()
    description = models.TextField()
    class Meta:
        db_table = u'variable'
    def __unicode__(self):
        return self.name

class Experiment(models.Model):
    id = models.IntegerField(primary_key=True)
    at_time = models.DateTimeField()
    by_user = models.TextField()
    on_host = models.TextField()
    model = models.ForeignKey(Model, db_column='model')
    class Meta:
        db_table = u'experiment'
    def __unicode__(self):
        return u'experiment'

class DefinedFor(models.Model):
    model = models.ForeignKey(Model, db_column='model')
    parameter = models.ForeignKey(Parameter, db_column='parameter')
    class Meta:
        db_table = u'defined_for'

class TaggedWith(models.Model):
    experiment = models.ForeignKey(Experiment, db_column='experiment')
    tag = models.ForeignKey(Tag, db_column='tag')
    class Meta:
        db_table = u'tagged_with'

class ParamValue(models.Model):
    experiment = models.ForeignKey(Experiment, db_column='experiment')
    parameter = models.ForeignKey(Parameter, db_column='parameter')
    at_time = models.FloatField()
    value = models.FloatField()
    of_interest = models.BooleanField()
    class Meta:
        db_table = u'param_value'

class VarValue(models.Model):
    experiment = models.ForeignKey(Experiment, db_column='experiment')
    variable = models.ForeignKey(Variable, db_column='variable')
    at_time = models.FloatField()
    value = models.FloatField()
    why_now = models.IntegerField()
    of_interest = models.BooleanField()
    class Meta:
        db_table = u'var_value'
