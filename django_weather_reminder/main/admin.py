from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserModel)
admin.site.register(CityModel)
admin.site.register(CountryModel)
admin.site.register(PeriodModel)
admin.site.register(SubscribersModel)
admin.site.register(EmailSubjectModel)
