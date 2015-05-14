function getDayHeader(day) {
	return '\
	<div class="row">\
		<div class="span12" id="day-header-' + day + '"><strong>Day ' + day + '</strong> &mdash; Total: &euro; 0.00</div>\
	</div>\
	';
}

/*
function getDayStyle(day) {
	var style;
	var color;
	var date = new Date().clearTime();

	date.set({ year: {{ year }}, month:({{ month }} -1), day:day});
	color = day_colors[day];
	if (!color) {
		if (date.getDay() === 0) {
			color = 'DDDDFF';
		} else if (date.getDay() === 6) {
			color = 'EEEEFF';
		}
	} else {
		if (date.getDay() === 0) {
			color = 'BBBBFF';
		} else if (date.getDay() === 6) {
			color = 'CCCCFF';
		}
	}
	if (color) {
		style = ' style="background-color: #' + color + ';"';
	} else {
		style = ''
	}
	return style;
}
*/

function putSpending(day, descr, amount, type, spid, payment) {
	var text = getFilledDaySpending(day, spid, descr, amount, type, payment);
	$('.spending_day_' + day).last().before(text);
}

function remove(spending) {
	var row = $('#btn_remove_' + spending).parent().parent();
	row.slideUp();
	$('#input_descr_' + spending).val('');
	$('#input_amount_' + spending).val('');
	$('#input_type_' + spending).val('');
	$('#input_payment_' + spending).val('');
}

function upDescr(obj) {
	var row = $(obj).parent().parent();
	var prev = row.prev();
	if (prev.size() === 0) {
		return;
	}
	var input = prev.find('.input_descr');
	if (input.size() === 0) {
		prev = prev.prev();
		input = prev.find('.input_descr');
	}
	input.focus();
	window.scrollTo(0, input.offset().top - 100);
}
function downDescr(obj) {
	var row = $(obj).parent().parent();
	var next = row.next();
	if (next.size() === 0) {
		return;
	}
	var input = next.find('.input_descr');
	if (input.size() === 0) {
		next = next.next();
		input = next.find('.input_descr');
	}
	input.focus();
	window.scrollTo(0, input.offset().top - 100);
}

function upAmount(obj) {
	var row = $(obj).parent().parent().parent();
	var prev = row.prev();
	if (prev.size() === 0) {
		return;
	}
	var input = prev.find('.input_amount');
	if (input.size() === 0) {
		prev = prev.prev();
		input = prev.find('.input_amount');
	}
	input.focus();
	window.scrollTo(0, input.offset().top - 100);
}
function downAmount(obj) {
	var row = $(obj).parent().parent().parent();
	var next = row.next();
	if (next.size() === 0) {
		return;
	}
	var input = next.find('.input_amount');
	if (input.size() === 0) {
		next = next.next();
		input = next.find('.input_amount');
	}
	input.focus();
	window.scrollTo(0, input.offset().top - 100);
}

function upType(obj) {
	var row = $(obj).parent().parent();
	var prev = row.prev();
	if (prev.size() === 0) {
		return;
	}
	var input = prev.find('.input_category');
	if (input.size() === 0) {
		prev = prev.prev();
		input = prev.find('.input_category');
	}
	input.focus();
	window.scrollTo(0, input.offset().top - 100);
}
function downType(obj) {
	var row = $(obj).parent().parent();
	var next = row.next();
	if (next.size() === 0) {
		return;
	}
	var input = next.find('.input_category');
	if (input.size() === 0) {
		next = next.next();
		input = next.find('.input_category');
	}
	input.focus();
	window.scrollTo(0, input.offset().top - 100);
}

function setFormDate() {
	var date = $('#select_date').val();
	var month = date.substring(0, date.indexOf('/'));
	var year = date.substring(date.indexOf('/') + 1);
	$('#input_month').val(month);
	$('#input_year').val(year);
}

function checkAndUpdateTotal(spending) {
	var input = $('#input_amount_' + spending);
	var val = parseFloat(input.val());
	var day;
	if (isNaN(val)) {
		input.addClass('error');
	} else {
		input.removeClass('error');
		input.val(val.toFixed(2));
	}
	day = $('#input_day_' + spending).val();
	updateDayTotal(day);
}

function updateDayTotal(day) {
	var total = 0;
	$('.spending_day_' + day).each(function (i, elem) {
		var input = $(elem).find('.input_amount');
		var val = parseFloat(input.val());
		if (!isNaN(val)) {
			total += val;
		}
	});
	$('#day-header-' + day).html('<strong>Day ' + day + '</strong> &mdash; Total: &euro; ' + total.toFixed(2));
}
