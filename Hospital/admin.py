from django.contrib import admin
from Hospital.models import Hospital,Doctors,Timing
# Register your models here.

admin.site.register(Hospital)
admin.site.register(Doctors)
admin.site.register(Timing)