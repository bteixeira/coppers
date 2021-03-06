# coding=utf-8

from django.shortcuts import render

import csv
from django.core.urlresolvers import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import  render_to_response
from django.template import RequestContext, loader, Context
from .models import *
from django.contrib.auth.decorators import login_required
import datetime
import string
from datetime import *
import StringIO
from .unicoder import *
# import version
import calendar
from django.contrib import messages

@login_required
def index(request):
	return HttpResponseRedirect(reverse('app.views.month_view'))


@login_required
def add_form(request):
    return render_to_response('add.htm', context_instance=RequestContext(request))


def get_day_colors(month, year):
	periods_start = Period.objects.filter(start__year=year, start__month=month)
	periods_end = Period.objects.filter(end__year=year, end__month=month)
	colors = {}
	for period in periods_start:
		for i in range(period.start.day, period.end.day + 1):
			if not colors.has_key(i):
				colors[i] = period.type.color
	for period in periods_end:
		for i in range(period.start.day, period.end.day + 1):
			if not colors.has_key(i):
				colors[i] = period.type.color
	return colors


@login_required
def about(request):
	return render_to_response('about.htm', context_instance=RequestContext(request))


@login_required
def month_view(request):
	if Spending.objects.exists():
		dateStart = Spending.objects.order_by('date')[0].date
		dateEnd = Spending.objects.order_by('-date')[0].date
	else:
		dateStart = datetime.now()
		dateEnd = dateStart
	dates = []
	m = dateStart.month
	y = dateStart.year
	dates.append({'month': m, 'year': y})
	while m != dateEnd.month or y != dateEnd.year:
		m = (m % 12) + 1
		if m == 1:
			y += 1
		dates.append({'month': m, 'year': y})
	if not request.GET.get('month', False):
		month = int(datetime.now().month)
	else:
		month = int(request.GET['month'])
	if not request.GET.get('year', False):
		year = int(datetime.now().year)
	else:
		year = int(request.GET['year'])
	if month == 12:
		month_next = 1
		month_next_year = year + 1
		month_prev = 11
		month_prev_year = year
	elif month == 1:
		month_next = 2
		month_next_year = year
		month_prev = 12
		month_prev_year = year - 1
	else:
		month_next = month + 1
		month_prev = month - 1
		month_prev_year = month_next_year = year
	year_next = year + 1
	year_prev = year - 1
	spendings_x = request.user.spending_set.filter(date__month=month, date__year=year).order_by('date')
	days = {}
	days_of_month = calendar.monthrange(year, month)[1]
	for day in range(1, days_of_month + 1):
		spendings = request.user.spending_set.filter(date__day=day, date__month=month, date__year=year)
		total = 0
		obj = {}
		for spending in spendings:
			total = total + spending.value
		obj['total'] = total
		obj['spendings'] = spendings
		days[day] = obj

	day_colors = get_day_colors(month, year)
	payment_types = PaymentType.objects.order_by('name')
	return render_to_response('month_view.htm',
			{'month': month, 'year': year,
			 'month_prev': month_prev,
			 'month_next': month_next,
			 'month_prev_year': month_prev_year,
			 'month_next_year': month_next_year,
			 'year_prev': year_prev,
			 'year_next': year_next,
			 'spendings': spendings_x,
			 'days': days,
			 'day_colors': day_colors,
			 'payment_types': payment_types,
			 'dates': dates}, context_instance=RequestContext(request))


@login_required
def save(request):
	# TODO only allow saving one's own spendings
	month = int(request.POST['month'])
	year = int(request.POST['year'])
	i = 0
	while 'descr_' + str(i) in request.POST:
		print 'going for entry #' + str(i)
		descr = request.POST['descr_' + str(i)]
		amount = request.POST['amount_' + str(i)]
		type = request.POST['type_' + str(i)]
		if request.POST['payment_' + str(i)]:
			payment_type_id = int(request.POST['payment_' + str(i)])
		else:
			payment_type_id = None
		spid = request.POST['spid_' + str(i)]
		day = int(request.POST['day_' + str(i)])
		print '  values: \'' + descr + '\' ; \'' + amount + '\' ; \'' + type + '\' ; \'' + spid + '\' ; \'' + str(
			day) + '\''
		print '  spid is \'' + spid + '\''
		if spid:
			print '  exists'
			spending = Spending.objects.get(id=spid)
			print '  existing is ' + str(spending)
			if descr == '' and amount == '' and type == '':
				spending.delete()
				print '  deleted'
			else:
				if spending.description != descr:
					spending.description = get_description(descr)
				if amount:
					spending.value = amount
				if not type and spending.type is not None:
					spending.type = None
				elif spending.type is None or spending.type.description != type:
					print '  no type defined, or type has changed'
					spending.type = get_type(type)
				if payment_type_id:
					spending.payment_id = payment_type_id
				else:
					spending.payment = None
				spending.save()
				print '  saved'
		elif descr or amount or type:
			print '  not exists'
			if not amount:
				amount = 0
			payments = PaymentType.objects.filter(id=payment_type_id)
			if payments.exists():
				payment = payments[0]
			else:
				payment = None
			add_spending(descr, type, amount, year, month, day, payment, request.user)
			print '  saved'
		else:
			print '  no data'
		i += 1
	return HttpResponseRedirect(reverse('app.views.month_view') + '?year=' + str(year) + '&month=' + str(month))


@login_required
def stats(request):
	sums = {}
	totals = {}
	unassigned = {}
	keys = []
	spendings = request.user.spending_set.all()
	for spending in spendings:
		if not spending.type:
			type = None
		else:
			type = spending.type.description
		year = spending.date.year
		month = spending.date.month
		if not type:
			if not year in unassigned:
				unassigned[year] = {}
			if not month in unassigned[year]:
				unassigned[year][month] = 0
			unassigned[year][month] += spending.value
		else:
			if not year in sums:
				sums[year] = {}
			if not month in sums[year]:
				sums[year][month] = {}
			if not type in sums[year][month]:
				sums[year][month][type] = 0
			sums[year][month][type] += spending.value
			if not type in keys:
				keys.append(type)
		if not year in totals:
			totals[year] = {}
		if not month in totals[year]:
			totals[year][month] = 0
		totals[year][month] += spending.value
	keys = sorted(keys)
	blabla = []
	for year in sorted(sums.keys()):
		for month in sorted(sums[year].keys()):
			list = [year, month, []]
			list[2].append(totals[year][month])
			if year in unassigned and month in unassigned[year]:
				list[2].append(unassigned[year][month])
			else:
				list[2].append(0)
			for key in keys:
				if key in sums[year][month]:
					list[2].append(sums[year][month][key])
				else:
					list[2].append(0)
			blabla.append(list)
	keys = ['Total', 'Sem Descr'] + keys
	print 'keys: ' + str(keys)
	print 'totals: ' + str(blabla)
	return render_to_response('stats.htm',
			{'keys': keys, 'totals': blabla},
			                  context_instance=RequestContext(request))

### Returns the Description model object for the given string. If there is more
### than one (which should not happen) it returns the first one
def get_description(descr):
	spDescrs = SpendingDescription.objects.filter(description=descr)
	if not spDescrs.exists():
		spDescr = SpendingDescription(description=descr)
		spDescr.save()
	else:
		spDescr = spDescrs[0]
	return spDescr


def get_type(type):
	spTypes = SpendingType.objects.filter(description=type)
	if not spTypes.exists():
		spType = SpendingType(description=type)
		spType.save()
	else:
		spType = spTypes[0]
	return spType


def add_spending(description, type, value, year, month, day, payment, user):
	spDescr = get_description(description)
	spType = get_type(type)
	sp = Spending(description=spDescr, type=spType, value=value, date=date(year, month, day), payment=payment,
	              user=user)
	sp.save()


@login_required
def importCSV(request):
	added = 0
	text = request.POST['spendings']
	sio = StringIO.StringIO(text)
	#reader = csv.reader(sio)
	#reader = UnicodeReader(sio)
	reader = unicode_csv_reader(sio)
	for line in reader:
		date = datetime.strptime(line[0], '%Y-%m-%d')
		#print line
		#descr = get_description(line[1])
		descr = line[1]
		#value = float(line[2])
		value = line[2]
		#type = get_type(line[3])
		type = line[3]
		#		if line[4].isdigit():
		#			payment = PaymentType.objects.get(id=line[4])
		if line[4] == '':
			payment = None
		else:
			payments = PaymentType.objects.filter(name=line[4])
			if payments.exists():
				payment = payments[0]
			else:
				payment = PaymentType(name=line[4])
				payment.save()
			#		else:
			#			payment = None
		add_spending(descr, type, value, date.year, date.month, date.day, payment, request.user)
		added += 1
	#	lines = text.splitlines()
	#	lines = filter(lambda str : str != '', lines)
	#	added = ignored = 0
	#	print ' lines: ' + str(lines)
	#	for line in lines:
	#		args = string.split(line, ';')
	#		print '  args: ' + str(args)
	#		args = [arg.strip() for arg in args]
	#		print '  args: ' + str(args)
	#		args = [arg.strip("'") for arg in args]
	#		print '  args: ' + str(args)
	#		if len(args) == 6:
	#			add_spending(args[1], args[3], args[4], request.user)
	#			added += 1
	#		else:
	#			ignored += 1
	#			print 'IGNORING: ' + str(args)
	#	print 'added: ' + str(added)
	#	print 'ignored: ' + str(ignored)
	ignored = 0
	return render_to_response('import_done.htm', {'added': added, 'ignored': ignored},
	                          context_instance=RequestContext(request))


@login_required
def importCSV_form(request):
	return render_to_response('importCSV_form.htm', context_instance=RequestContext(request))


@login_required
def exportCSV(request):
	# https://docs.djangoproject.com/en/1.2/howto/outputting-csv/
	# using the template system because it's cleanner for Unicode chars
	response = HttpResponse(content_type='text/csv')
	now = datetime.now()
	response['Content-Disposition'] = 'attachment; filename=export_' + now.strftime("%Y_%m_%d_%H%M%S") + '.csv'
	#writer = csv.writer(response)
	writer = UnicodeWriter(response)

	#csv_data =
	header = [
		#(
		'Date', 'Description', 'Value', 'Type', 'Payment Type'
		#)
	]
	writer.writerow(header)
	spendings = request.user.spending_set.all()
	for spending in spendings:
		if spending.description is None:
			description = ''
		else:
			description = spending.description.description

		if spending.type is None:
			type = ''
		else:
			type = spending.type.description

		if spending.payment is None:
			payment = ''
		else:
			payment = spending.payment.name

		#		csv_data.append(
		#	(
		#writer.writerow([spending.date.strftime('%Y-%m-%d'), description.encode('utf-8'), spending.value, type.encode('utf-8'), payment.encode('utf-8')])
		writer.writerow([spending.date.strftime('%Y-%m-%d'), description, str(spending.value), type, payment])
	#		)


	#	t = loader.get_template('csv_template.txt')
	#	c = Context({
	#	    'data': csv_data,
	#	})
	#	response.write(t.render(c))
	return response


@login_required
def report_cash(request):
	user_spendings = request.user.spending_set
	start = datetime.now() - timedelta(days=1)
	if request.POST.get('date_start'):
		start = datetime.strptime(request.POST.get('date_start'), '%Y-%m-%d')
	user_spendings = user_spendings.filter(date__gte=start)
	end = datetime.now() - timedelta(days=1)
	if request.POST.get('date_end'):
		end = datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d')
	user_spendings = user_spendings.filter(date__lte=end)
	payments = PaymentType.objects.all()
	payment_filter = []
	payment_inputs = []
	for payment in payments:
		pid = request.POST.get('payment_' + str(payment.id))
		if pid:
			payment_filter.append(payment.id)
		p_input = {}
		p_input['id'] = payment.id
		p_input['name'] = payment.name
		p_input['checked'] = pid
		payment_inputs.append(p_input)
	print('payment filters: ' + str(payment_filter))
	if payment_filter:
		user_spendings = user_spendings.filter(payment__in=payment_filter)
	spendings_raw = user_spendings.order_by('date')
	spendings = []
	total = 0
	for spending in spendings_raw:
		total += spending.value
		if spending.description is None:
			descr = ''
		else:
			descr = spending.description.description
		if spending.type is None:
			type = ''
		else:
			type = spending.type.description
		if spending.payment is None:
			payment = ''
		else:
			payment = spending.payment.name
		spendings.append({
			'total': total,
			'date': spending.date,
			'value': spending.value,
			'descr': descr,
			'type': type,
			'payment': payment
		})
	params = {
		'spendings': spendings,
		'payments': payment_inputs
	}
	params['start'] = start
	params['end'] = end
	return render_to_response('report_cash.htm', params, context_instance=RequestContext(request))


@login_required
def get_descriptions(request):
	descriptions = SpendingDescription.objects.all().order_by('description')
	term = request.GET.get('term')
	if term:
		descriptions = descriptions.filter(description__istartswith=term)
	limit = request.GET.get('limit')
	if limit is None:
		descriptions = descriptions[:10]
	elif int(limit) > 0:
		descriptions = descriptions[:limit]
	return render_to_response('array.json.htm', {
		'descriptions': descriptions
	}, context_instance=RequestContext(request))


@login_required
def get_types(request):
	descriptions = SpendingType.objects.all().order_by('description')
	term = request.GET.get('term')
	if term:
		descriptions = descriptions.filter(description__istartswith=term)
	limit = request.GET.get('limit')
	if limit is None:
		descriptions = descriptions[:10]
	elif int(limit) > 0:
		descriptions = descriptions[:limit]
	return render_to_response('array.json.htm', {
		'descriptions': descriptions
	}, context_instance=RequestContext(request))

@login_required
def month_pie(request):
	month = request.GET.get('month')
	if month is None:
		month = request.POST.get('month')
	if month is None:
		month = 2
	year = request.GET.get('year')
	if year is None:
		year = request.POST.get('year')
	if year is None:
		year = 2012
	spendings = request.user.spending_set.filter(date__month=month, date__year=year)
	data = {'[SEM TIPO]': 0}
	for spending in spendings:
		if spending.type is None:
			total = data['[SEM TIPO]']
			total += spending.value
			data['[SEM TIPO]'] = total
		else:
			type = spending.type.description
			if type in data:
				total = data[type]
				total += spending.value
				data[type] = total
			else:
				data[type] = spending.value

	return render_to_response('month_pie.htm', {
		'data': data
	}, context_instance=RequestContext(request))

@login_required
def personal(request):
	return render_to_response('personal.htm', {'version': version.VERSION},
	                          context_instance=RequestContext(request))

@login_required
def change_password(request):
	args = {}
	if request.POST['password'] == request.POST['password-confirm']:
		request.user.set_password(request.POST['password'])
		request.user.save()
		messages.success(request, 'Password changed')
		return HttpResponseRedirect(reverse('app.views.personal'))
	else:
		messages.error(request, 'Passwords do not match')
		return render_to_response('personal.htm', args,
	                          context_instance=RequestContext(request))
