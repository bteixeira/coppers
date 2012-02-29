from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.views import *
from gastosapp.models import *

urlpatterns = patterns('',
	(r'^$', 'gastosapp.views.index'),
#	(r'^index$', 'gastosapp.views.index'),
	#(r'^login$', 'gastosapp.views.login'),
	(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'gastosapp/login.htm'}),
#	(r'^logout$', 'gastosapp.views.logout'),
	(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
	(r'^month_view$', 'gastosapp.views.month_view'),
	(r'^save$', 'gastosapp.views.save'),
	(r'^import_form$', 'gastosapp.views.import_form'),
	(r'^import$', 'gastosapp.views.import_spendings'),
	(r'^stats$', 'gastosapp.views.stats'),
	(r'^export$', 'gastosapp.views.export'),
	(r'^exportCSV$', 'gastosapp.views.exportCSV'),
	(r'^month_graph$', 'gastosapp.views.exportCSV'),
	(r'^report_cash$', 'gastosapp.views.report_cash'),
	(r'^media/(?P<path>.*\.js)$', 'django.views.static.serve', {'document_root': 'gastosapp/media/js/'}),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'gastosapp/media/'}),
)

