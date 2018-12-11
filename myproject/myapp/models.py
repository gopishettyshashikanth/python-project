from django.db import models

# Create your models here.

class Patient(models.Model):
   
    registration_number = models.CharField(max_length=100,blank=True, null=True)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    visit_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    

    class Meta:
        verbose_name_plural = "Patient"
        verbose_name = 'Patient'
    
    def __str__(self):
        return '%s' % self.registration_number

class customers(models.Model):
   
    item = models.CharField(max_length=100,blank=True, null=True)
    qty = models.CharField(max_length=250, blank=True, null=True)
    size = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=250, blank=True, null=True)
    

    class Meta:
        verbose_name_plural = "customers"
        verbose_name = 'customers'
    
    def __str__(self):
        return '%s' % self.qty        
