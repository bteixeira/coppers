from django.conf.urls.defaults import *
from gastosapp.models import *

urlpatterns = patterns('',
	(r'^$', 'gastosapp.views.index'),
	(r'^login$', 'gastosapp.views.login'),
	(r'^logout$', 'gastosapp.views.logout'),
	(r'^month_view$', 'gastosapp.views.month_view'),
	(r'^save$', 'gastosapp.views.save'),
	(r'^import_form$', 'gastosapp.views.import_form'),
	(r'^import$', 'gastosapp.views.import_spendings'),
	(r'^stats$', 'gastosapp.views.stats'),
	(r'^export$', 'gastosapp.views.export'),
	(r'^exportCSV$', 'gastosapp.views.exportCSV'),
	(r'^month_graph$', 'gastosapp.views.exportCSV'),
	(r'^report_cash$', 'gastosapp.views.report_cash'),
<<<<<<< HEAD
	(r'^media/(?P<path>.*\.js)$', 'django.views.static.serve', {'document_root': 'gastosapp/media/js'}),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'gastosapp/media'}),
=======
	(r'^media/(?P<path>.*\.js)$', 'django.views.static.serve', {'document_root': '/home/acat/projects/gastos/gastosapp/media/js'}),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/acat/projects/gastos/gastosapp/media'}),
>>>>>>> 3de71b2bdaa31bc3db1a3696f1537fa5662b2445
)
