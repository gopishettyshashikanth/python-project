from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from myapp.myapp_serializers import *
from datetime import datetime, date, timedelta
import redis
import json
import ast
import sys
from django.http import Http404, HttpResponse
import csv
import pymongo

# Create your views here.
class CustomAPIResponse():
    """docstring for ClassName"""
    def __init__(self, **kwargs):
        self.response = {
                "success" : kwargs.get('success'),
                "errors"  : kwargs.get('errors',{}),
                "data": kwargs.get('data', {}),
            }

class PatientViewSet(APIView):
    def post(self,request,format=None):
        serializer = AppointmentSerializer(data=request.data)
        visit_date =  datetime.now().strftime("%Y-%m-%d") 
        try:
            patient_obj = Patient.objects.get(registration_number=request.data['registration_number'])
        except Exception as e:
            patient_obj = None

        if serializer.is_valid():
            try:   
                redisClient = redis.StrictRedis(host='localhost',port=6379,db=10)
                kwargs = { 
                    "registration_number":request.data['registration_number'],
                    "first_name":request.data['first_name'],                    
                    "visit_date":visit_date,
                    "location":request.data['location'] 
                    }

                redisClient.rpush('patient_list', kwargs)

                if patient_obj == None:                    
                    queryset = Patient.objects.create(**kwargs)
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

class PatientCacheViewSet(APIView):
    def get(self,request,registration_number):
        redisClient = redis.StrictRedis(host='localhost',port=6379,db=10)
        # context_data = {"success" : True, "data" : {"status" : redisClient.hget(registration_number,'status'),"registration_number" : redisClient.hget(registration_number,'registration_number')}}
        context_data = {"success" : True, "data" : {"status" : redisClient.hgetall(registration_number)}}
        return Response(CustomAPIResponse(**context_data).response)        

class PatientDetailsCacheViewSet(APIView):
    def get(self,request):
        output_details_list=[]
        redisClient = redis.StrictRedis(host='localhost',port=6379,db=10)
        details_list =  redisClient.lrange('patient_list',0,-1)
        for each in details_list:            
            output_details_list.append(ast.literal_eval(each))
        print output_details_list,"output_details_list"    
        context_data = {"success" : True, "data" : {"status" : output_details_list}}
        return Response(CustomAPIResponse(**context_data).response) 

class PatientDetailsViewSet(APIView):
    def get(self,request):
        queryset = Patient.objects.all()            
        patient_list = queryset.values('first_name','visit_date','registration_number','location')
        context_data = {"success" : True, "data" :{"patient_list":patient_list, "total" : queryset.count(), "message" : "%s Records Found" %(queryset.count())}}
        return Response(CustomAPIResponse(**context_data).response)

def PatientDetailsCsvViewSet(request):
    queryset = Patient.objects.all()            
    csv_data = queryset.values('first_name','visit_date','registration_number','location')
    reload(sys)
    sys.setdefaultencoding('utf8')
    response = HttpResponse(content_type='text/csv')
    current_date = datetime.now().strftime("%Y-%m-%d : %H-%M-%S %p")
    filename = "Patient-Report-Download_{0}.csv".format(current_date)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    # fieldnames = csv_data[0].keys()
    
    fieldnames = ['first_name', 'visit_date','registration_number','location']
    writer = csv.writer(response)
    writer.writerow(fieldnames)
    for each_dict in csv_data:
        value = each_dict.values()
        writer.writerow(list(value))

    return response

def PatientDetailsCsvCacheViewSet(request):
    csv_data=[]
    redisClient = redis.StrictRedis(host='localhost',port=6379,db=10)
    details_list =  redisClient.lrange('patient_list',0,-1)
    
    for each in details_list:            
        csv_data.append(ast.literal_eval(each))

    reload(sys)
    sys.setdefaultencoding('utf8')
    response = HttpResponse(content_type='text/csv')
    current_date = datetime.now().strftime("%Y-%m-%d : %H-%M-%S %p")
    filename = "Patient-Report-Download_{0}.csv".format(current_date)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        
    fieldnames = ['first_name', 'visit_date','registration_number','location']
    writer = csv.writer(response)
    writer.writerow(fieldnames)
    for each_dict in csv_data:
        value = each_dict.values()
        writer.writerow(list(value))

    return response



#mongo db
class CustomersViewSet(APIView):
    def post(self,request,format=None):
        serializer = CustomrtSerializer(data=request.data)
        visit_date =  datetime.now().strftime("%Y-%m-%d") 
        if serializer.is_valid():
            try: 
                myclient = pymongo.MongoClient('mongodb://localhost:27017/')
                db = myclient['mydatabase']  

                kwargs = { 
                    "item":request.data['item'],
                    "qty":request.data['qty'],                    
                    "size":request.data['size'],
                    "status":request.data['status'] 
                    }
                x = db.customers.insert_one(kwargs)  
                print x,"----"
                context_data = {"success" : True, "data" :{"message" : "Record Created Successfully"}}     
            except Exception as e:
                print e
                context_data = {"success" : False, "errors" : {"message":str(e)}}
                pass                     
        else:
            errors_list =  format_serializer_errors(**serializer.errors)
            context_data = {"success" : False, "errors" : {"message": "Validation Error" ,  "errors_list" : errors_list}}
        return Response(CustomAPIResponse(**context_data).response)

class CustomersGetViewSet(APIView):
    def get(self,request):      
        output_details_list=[]  
        myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        db = myclient['mydatabase'] 
        for x in db.customers.find():    
            x.pop('_id')         
            output_details_list.append(x)

        print output_details_list,"+++++"    
        
        context_data = {"success" : True, "data" : {"status" : output_details_list}}
        return Response(CustomAPIResponse(**context_data).response) 
