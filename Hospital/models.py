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


class Timing(models.Model):
    time = models.CharField(max_length=20)
    is_booked = models.BooleanField()

