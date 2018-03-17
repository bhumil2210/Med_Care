from django.contrib import admin
from Hospital.models import Hospital, Doctors, Records, Medicine

# Register your models here.

admin.site.register(Hospital)
admin.site.register(Doctors)
admin.site.register(Records)
admin.site.register(Medicine)