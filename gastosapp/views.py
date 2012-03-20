# coding=utf-8

import csv
from django.core.urlresolvers import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import  render_to_response
from django.template import RequestContext, loader, Context
from gastosapp.models import *
from django.contrib.auth.decorators import login_required
import datetime
import string
from datetime import *
import StringIO
from gastosapp.unicoder import *
import version

@login_required
def index(request):
	return HttpResponseRedirect(reverse('gastosapp.views.month_view'))

def get_day_colors(month, year):
	periods_start = Period.objects.filter(start__year=year,start__month=month)
	periods_end = Period.objects.filter(end__year=year,end__month=month)
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
	return render_to_response('gastosapp/about.htm', {'version': version.VERSION}, context_instance=RequestContext(request))

@login_required
def month_view(request):
	code = 'bteixeira'
	if Spending.objects.exists():	
		dateStart = Spending.objects.order_by('date')[0].date
		dateEnd = Spending.objects.order_by('-date')[0].date
	else:
		dateStart = datetime.now()
		dateEnd = dateStart
	print 'start date: ' + str(dateStart)
	print 'end date: ' + str(dateEnd)
	dates = []
	m = dateStart.month
	y = dateStart.year
	print '!!! ' + str(m) + '/' + str(y)
	dates.append({'month': m, 'year': y})
	while m != dateEnd.month or y != dateEnd.year:
		m = (m % 12) + 1
		if m == 1:
			y += 1
		dates.append({'month': m, 'year': y})
		print '!!! ' + str(m) + '/' + str(y)
	if not request.GET.get('month',False):
		month = int(datetime.now().month)
	else:
		month = int(request.GET['month'])
	if not request.GET.get('year',False):
		year = int(datetime.now().year)
	else:
		year = int(request.GET['year'])
	print 'month: ' + str(month)
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
	print 'code: ' + str(code)
	spendings = request.user.spending_set.filter(date__month=month,date__year=year)
	day_colors = get_day_colors(month, year)
	payment_types = PaymentType.objects.order_by('name')
	print spendings
	return render_to_response('gastosapp/month_view.htm',
							{'month': month, 'year': year,
							'month_prev': month_prev,
							'month_next': month_next,
							'month_prev_year': month_prev_year,
							'month_next_year': month_next_year,
							'year_prev': year_prev,
							'year_next': year_next,
							'spendings': spendings,
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
		print '  values: \'' + descr + '\' ; \'' + amount + '\' ; \'' + type + '\' ; \'' + spid + '\' ; \'' + str(day) + '\''
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
			payment = PaymentType.objects.get(id=payment_type_id)
			add_spending(descr,type,amount,year,month,day,payment,request.user)
			print '  saved'
		else:
			print '  no data'
		i += 1
	return HttpResponseRedirect(reverse('gastosapp.views.month_view') + '?year=' + str(year) + '&month=' + str(month))
	
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
	return render_to_response('gastosapp/stats.htm',
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
	sp = Spending(description=spDescr, type=spType, value=value, date=date(year,month,day), payment=payment, user=user)
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
		payment = get_payment_by_id(line[4])
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
	return render_to_response('gastosapp/import_done.htm', {'added':added, 'ignored':ignored}, context_instance=RequestContext(request))

@login_required
def importCSV_form(request):
	return render_to_response('gastosapp/importCSV_form.htm', context_instance=RequestContext(request))

@login_required
def exportCSV(request):
	# https://docs.djangoproject.com/en/1.2/howto/outputting-csv/
	# using the template system because it's cleanner for Unicode chars
	response = HttpResponse(mimetype='text/csv')
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

	
#	t = loader.get_template('gastosapp/csv_template.txt')
#	c = Context({
#	    'data': csv_data,
#	})
#	response.write(t.render(c))
	return response

@login_required
def report_cash(request):
	if not request.GET.get('payment',False):
		payments = ['Dinheiro']
	else:
		payments = request.GET['payment'].split(',')

	if not request.GET.get('month',False):
		month = int(datetime.now().month)
	else:
		month = int(request.GET['month'])

	if not request.GET.get('year',False):
		year = int(datetime.now().year)
	else:
		year = int(request.GET['year'])

	user_spendings = request.user.spending_set
	spendings_raw = user_spendings.filter(date__month=month,date__year=year,payment__name__in=payments).order_by('date')
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
		spendings.append({
			'total': total,
		    'date': str(spending.date),
		    'value': spending.value,
		    'descr': descr,
		    'type': type
		})
	return render_to_response('gastosapp/report_cash.htm', {
		'spendings': spendings,
	    'month': month,
	    'year': year,
	    'payments': ', '.join(payments)
	}, context_instance=RequestContext(request))
