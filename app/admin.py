from django.contrib import admin
from .models import *

admin.site.register(Code)
admin.site.register(CodeInfo)
admin.site.register(SpendingType)
admin.site.register(SpendingDescription)
admin.site.register(SpendingLocation)
admin.site.register(Spending)
admin.site.register(PeriodType)
admin.site.register(Period)
admin.site.register(PaymentType)

