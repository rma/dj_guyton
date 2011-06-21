import os

from django.conf.urls.defaults import *
from django.views.generic import list_detail

from guyton.models import Parameter, Variable, Tag

par_info = {
    'queryset': Parameter.objects.order_by('name'),
    'template_name': 'parameter_list.html',
}
var_info = {
    'queryset': Variable.objects.order_by('name'),
    'template_name': 'variable_list.html',
}
tag_info = {
    'queryset': Tag.objects.order_by('name'),
    'template_name': 'tag_list.html',
}

urlpatterns = patterns('guyton.views',
    (r'^$', 'index'),
    (r'^params/$', list_detail.object_list, par_info),
    (r'^vars/$', list_detail.object_list, var_info),
    (r'^tags/$', list_detail.object_list, tag_info),
    (r'^details/$', 'list_details'),
    (r'^tasks/(?P<task_hash>[0-9a-f]{64})/$', 'show_task'),
)

urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': os.path.join(os.path.dirname(__file__), 'site_media')}),
)
