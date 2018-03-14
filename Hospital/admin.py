from django.contrib import admin
from Hospital.models import Hospital,Doctors,Records
# Register your models here.

admin.site.register(Hospital)
admin.site.register(Doctors)
admin.site.register(Records)