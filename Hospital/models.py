from django.db import models

# Create your models here.


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    Address1 = models.CharField(max_length=250)
    Address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.IntegerField()
    no_of_beds_available = models.IntegerField(default=0)
    total_beds = models.IntegerField(default=0)
    type1 = models.IntegerField(default=0)
    type2 = models.IntegerField(default=0)
    type3 = models.IntegerField(default=0)

    objects = models.Manager()

    @staticmethod
    def get_queryset():
        return Hospital.objects.all()


class Doctors(models.Model):
    Hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    Speciality = models.CharField(max_length=250)
    app_no = models.CharField(max_length=250)


class Records(models.Model):
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=250)
    contact_no = models.IntegerField()
    Address = models.CharField(max_length=250)
    Doctor_attending = models.CharField(max_length=250)
    Appointment_no = models.CharField(max_length=250)
    is_checked_out = models.CharField(max_length=10)
    type1 = models.CharField(max_length=10)
    type2 = models.CharField(max_length=10)
    type3 = models.CharField(max_length=10)
