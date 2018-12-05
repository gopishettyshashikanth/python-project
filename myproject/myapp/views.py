from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from myapp.myapp_serializers import *
from datetime import datetime, date, timedelta
import redis

# Create your views here.
class CustomAPIResponse():
    """docstring for ClassName"""
    def __init__(self, **kwargs):
        self.response = {
                "success" : kwargs.get('success'),
                "errors"  : kwargs.get('errors',{}),
                "data": kwargs.get('data', {}),
            }

class AppointmentViewSet(APIView):
    def post(self,request,format=None):
        serializer = AppointmentSerializer(data=request.data)
        visit_date =  datetime.now().strftime("%Y-%m-%d") 
        try:
            appointment_obj = Appointment.objects.get(registration_number=request.data['registration_number'])
        except Exception as e:
            appointment_obj = None

        if serializer.is_valid():
            try:   
                redisClient = redis.StrictRedis(host='localhost',port=6379,db=10)
                kwargs ={ 
                    "registration_number":request.data['registration_number'],
                    "status":request.data['status'],
                    "comments":request.data['comments'],
                    "visit_date":visit_date  
                    }
                                    
                if appointment_obj == None:                    
                    queryset = Appointment.objects.create(**kwargs)
                    key_name = "appointment_{0}".format(visit_date)
                    redisClient.rpush(key_name, request.data['registration_number'])
                    redisClient.hmset(request.data['registration_number'],kwargs)
                    context_data = {"success" : True, "data" :{"message" : "Record Created Successfully"}}
                else:
                    context_data = {"success" : True, "data" :{"message" : "Record already Exist"}}     
            except Exception as e:
                print e
                context_data = {"success" : False, "errors" : {"message":str(e)}}
                pass                     
        else:
            errors_list =  format_serializer_errors(**serializer.errors)
            context_data = {"success" : False, "errors" : {"message": "Validation Error" ,  "errors_list" : errors_list}}
        return Response(CustomAPIResponse(**context_data).response)

class AppointmentDetailsCacheViewSet(APIView):
    def get(self,request,registration_number):
        redisClient = redis.StrictRedis(host='localhost',port=6379,db=10)
        
        context_data = {"success" : True, "data" : {"status" : redisClient.hget(registration_number,'status'),"registration_number" : redisClient.hget(registration_number,'registration_number')}}
        # context_data = {"success" : True, "data" : redisClient.hgetall(registration_number)}
        return Response(CustomAPIResponse(**context_data).response)        
