from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('api/receive-scan/', views.receive_scan, name='receive_scan'),
    path('api/get-scans/', views.get_scans, name='get_scans'),
    path('api/clear-scans/', views.clear_scans, name='clear_scans'),
]
