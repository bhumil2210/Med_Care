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
    Speciality = models.CharField(max_length=250,default=0, blank=True, null=True)
    current_app_no = models.CharField(max_length=250, default=0)
    assigned_app_no = models.CharField(max_length=250,default=0)


class Medicine(models.Model):
    name = models.CharField(max_length=250)
    price = models.CharField(max_length=250)
    location = models.CharField(max_length=250)


class Records(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=250,null=True,blank=True)
    contact_no = models.CharField(default=0, max_length=10,blank=True, null=True)
    Address = models.CharField(max_length=250, default=0, blank=True, null=True)
    Doctor_attending = models.CharField(max_length=250, default=0, blank=True, null=True)
    speciality = models.CharField(max_length=250, default=0, null=True, blank=True)
    type1 = models.CharField(max_length=10, default='N',blank=True,null=True)
    type2 = models.CharField(max_length=10, default='N',blank=True,null=True)
    type3 = models.CharField(max_length=10, default='N',blank=True,null=True)
