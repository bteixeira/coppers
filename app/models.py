from django.db import models
from django.contrib.auth.models import User

# Unused?
class Code(models.Model):
	code = models.CharField(max_length=32)
	metainfo = models.TextField()
	
	def __unicode__(self):
		return '[[' + self.code + ']]'

# Unused?
class CodeInfo(models.Model):
	code = models.ForeignKey(Code)
	key = models.CharField(max_length=32)
	value = models.CharField(max_length=256)

# Tags to apply to the spending
class SpendingType(models.Model):
	description = models.CharField(max_length=200)
	
	def __unicode__(self):
		return 'TYPE[' + self.description + ']'

# The description of the spending
# "had lunch with boss on the vietnamese around the corner from the office"
# Making this an entity makes it easier to reuse descriptions and group spendings by same description
class SpendingDescription(models.Model):
	description = models.CharField(max_length=200)
	
	def __unicode__(self):
		return '<' + self.description + '>'

# Unused?
class SpendingLocation(models.Model):
	description = models.CharField(max_length=200)

# The "account" from which you paid this
# Intended for values like "pocket money", "savings account", "visa credit card"
class PaymentType(models.Model):
	name = models.CharField(max_length=30)

	def __unicode__(self):
		return 'Pagamento:' + self.name

class Spending(models.Model):
	value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	description = models.ForeignKey(SpendingDescription, null=True)
	location = models.ForeignKey(SpendingLocation, null=True, blank=True)
	details = models.CharField(max_length=200, null=True, blank=True)
	amount = models.CharField(max_length=200, null=True, blank=True)
	date = models.DateTimeField(null=True)
	type = models.ForeignKey(SpendingType, null=True, blank=True)
#	code = models.ForeignKey(Code, null=True)
	payment = models.ForeignKey(PaymentType, null=True, blank=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		result = '{SPENT ' + str(self.value) + ' @ ' + str(self.date)
		if self.description is not None:
			result += ' ON ' + self.description.__unicode__()
		result += '}'
		return result

# Unused?
class PeriodType(models.Model):
	name = models.CharField(max_length=30)
	color = models.CharField(max_length=6)

	def __unicode__(self):
		return self.name + ' (#' + self.color + ')'

# Unused?
class Period(models.Model):
	name = models.CharField(max_length=30)
	start = models.DateField()
	end = models.DateField()
	type = models.ForeignKey(PeriodType)

	def __unicode__(self):
		return self.type.name + ':' + self.name + ' (' + str(self.start) + ')'
