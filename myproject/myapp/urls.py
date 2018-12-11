from django.conf.urls import   url
from rest_framework.urlpatterns import format_suffix_patterns
from myapp.views import PatientViewSet,PatientDetailsCacheViewSet,PatientCacheViewSet,PatientDetailsViewSet,PatientDetailsCsvViewSet,PatientDetailsCsvCacheViewSet,CustomersViewSet,CustomersGetViewSet

urlpatterns = [
	
	url(r'^patients$', PatientViewSet.as_view(), name='patients_data_api'),
	url(r'^get_patients_cache/(?P<registration_number>[\w-]+)$', PatientCacheViewSet.as_view(), name='get_patients_details_cache_api'),
	
	url(r'^get_patients/$', PatientDetailsViewSet.as_view(), name='get_patients_details_api'),
	url(r'^get_patients/csv$', PatientDetailsCsvViewSet, name='get_patients_details_csv_api'),

	url(r'^get_patients_cache/$', PatientDetailsCacheViewSet.as_view(), name='get_patients_details_cache_api'),
	url(r'^get_patients_cache/csv/$', PatientDetailsCsvCacheViewSet, name='get_patients_details_cache_csv_api'),
	
	#mongo db
	url(r'^customers$', CustomersViewSet.as_view(), name='customers_data_api'),
	url(r'^customers_get$', CustomersGetViewSet.as_view(), name='customers_get_data_api'),

]