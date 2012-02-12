from django.db import models

class Code(models.Model):
	code = models.CharField(max_length=32)
	metainfo = models.TextField()
	
	def __unicode__(self):
		return '[[' + self.code + ']]'

class CodeInfo(models.Model):
	code = models.ForeignKey(Code)
	key = models.CharField(max_length=32)
	value = models.CharField(max_length=256)

class SpendingType(models.Model):
	description = models.CharField(max_length=200)
	
	def __unicode__(self):
		return 'TYPE[' + self.description + ']'

class SpendingDescription(models.Model):
	description = models.CharField(max_length=200)
	
	def __unicode__(self):
		return '<' + self.description + '>'

class SpendingLocation(models.Model):
	description = models.CharField(max_length=200)

class PaymentType(models.Model):
	name = models.CharField(max_length=30)

	def __unicode__(self):
		return 'Pagamento:' + self.name

class Spending(models.Model):
	value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	description = models.ForeignKey(SpendingDescription, null=True)
	location = models.ForeignKey(SpendingLocation, null=True)
	details = models.CharField(max_length=200, null=True)
	amount = models.CharField(max_length=200, null=True)
	date = models.DateTimeField(null=True)
	type = models.ForeignKey(SpendingType, null=True)
	code = models.ForeignKey(Code, null=True)
	payment = models.ForeignKey(PaymentType, null=True, blank=True)

	def __unicode__(self):
		result = '{SPENT ' + str(self.value) + ' @ ' + str(self.date)
		if self.description != None:
			result += ' ON ' + self.description.__unicode__()
		result += '}'
		return result
	
class PeriodType(models.Model):
	name = models.CharField(max_length=30)
	color = models.CharField(max_length=6)

	def __unicode__(self):
		return self.name + ' (#' + self.color + ')'

class Period(models.Model):
	name = models.CharField(max_length=30)
	start = models.DateField()
	end = models.DateField()
	type = models.ForeignKey(PeriodType)

	def __unicode__(self):
		return self.type.name + ':' + self.name + ' (' + str(self.start) + ')'
