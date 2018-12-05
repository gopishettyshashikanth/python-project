from django.conf.urls import   url
from rest_framework.urlpatterns import format_suffix_patterns
from myapp.views import AppointmentViewSet,AppointmentDetailsCacheViewSet

urlpatterns = [
	url(r'^appointments$', AppointmentViewSet.as_view(), name='appointment_data_api'),
	url(r'^get_appointment_cache/(?P<registration_number>[\w-]+)$', AppointmentDetailsCacheViewSet.as_view(), name='get_appointment_details_cache_api'),

]