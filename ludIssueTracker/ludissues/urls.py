from django.conf.urls import patterns, include, url

# use ludissues model from models import ludissues
# dictionary with all the objects in the ludissues
info = {
    'queryset': ludissues.objects.all()
}
# To save us writing lot of python code we are using the list_detail generic view
# list detail is the name of the view we are using
urlpatterns = patterns('django.views.generic.list_detail'),
    # issue-list and issue-detail are the template names
    # which will be looked in the default template directories
    url(r'^$', 'object_list', info, name='issue-list'),
    url(r'^(?P<object_id>\d+)/$', 'object_detail', info, name='issue-detail'),
)
