from django.db import models

# Create your models here.

class Appointment(models.Model):
   
    registration_number = models.CharField(max_length=100,blank=True, null=True)
    comments = models.CharField(max_length=250, blank=True, null=True)
    visit_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=250, blank=True, null=True)
    

    class Meta:
        verbose_name_plural = "Appointment"
        verbose_name = 'Appointment'
    
    def __str__(self):
        return '%s' % self.registration_number
