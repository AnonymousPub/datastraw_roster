from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('employees/', views.employee_list_view, name='employee_list'),
    path('brands/', views.brand_management_view, name='brand_management'),
    path('allocations/', views.resource_allocation_view, name='resource_allocation'),
    path('leaves/', views.leave_holiday_view, name='leave_holiday'),
    path('roster/generate/', views.generate_roster_view, name='generate_roster'),
    path('roster/<int:roster_id>/', views.roster_detail_view, name='roster_view'),
]