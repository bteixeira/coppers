from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.views import *
from gastosapp.models import *

urlpatterns = patterns('',
	(r'^$', 'gastosapp.views.index'),
	(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'gastosapp/login.htm'}),
	(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
	(r'^about$', 'gastosapp.views.about'),
	(r'^month_view$', 'gastosapp.views.month_view'),
	(r'^save$', 'gastosapp.views.save'),
	(r'^importCSV$', 'gastosapp.views.importCSV'),
	(r'^importCSV_form$', 'gastosapp.views.importCSV_form'),
	(r'^stats$', 'gastosapp.views.stats'),
	(r'^exportCSV$', 'gastosapp.views.exportCSV'),
	(r'^report_cash$', 'gastosapp.views.report_cash'),
	(r'^month_pie$', 'gastosapp.views.month_pie'),
	(r'^personal$', 'gastosapp.views.personal'),
	(r'^change_password$', 'gastosapp.views.change_password'),

    (r'^services/descriptions$', 'gastosapp.views.get_descriptions'),
    (r'^services/types', 'gastosapp.views.get_types'),

#	(r'^media/(?P<path>.*\.js)$', 'django.views.static.serve', {'document_root': 'gastosapp/media/js/'}),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'gastosapp/media/'}),
)
