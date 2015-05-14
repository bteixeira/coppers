from django.conf.urls import url
import django

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	url(r'^$', views.index),
	# url(r'^login$', django.contrib.auth.views.login, {'template_name': 'login.htm'}),
	url(r'^login$', auth_views.login, {'template_name': 'login.htm'}),
	url(r'^logout$', django.contrib.auth.views.logout_then_login),
	url(r'^about$', views.about),
	url(r'^month_view$', views.month_view),
	url(r'^save$', views.save),
	url(r'^importCSV$', views.importCSV),
	url(r'^importCSV_form$', views.importCSV_form),
	url(r'^stats$', views.stats),
	url(r'^exportCSV$', views.exportCSV),
	url(r'^report_cash$', views.report_cash),
	url(r'^month_pie$', views.month_pie),
	url(r'^personal$', views.personal),
	url(r'^change_password$', views.change_password),

    url(r'^services/descriptions$', views.get_descriptions),
    url(r'^services/types', views.get_types),

#	(r'^media/(?P<path>.*\.js)$', 'django.views.static.serve', {'document_root': 'gastosapp/media/js/'}),
	# url(r'^assets/(?P<path>.*)$', django.views.static.serve, {'document_root': 'assets/'}),
]
