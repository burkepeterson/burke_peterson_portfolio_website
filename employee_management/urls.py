from django.urls import path
from employee_management import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('form/', views.employee_form_request, name='employee_form'),
    path('delete/<int:item_id>/', views.employee_delete, name='employee_delete'),
    path('form/<int:item_id>/', views.employee_form_request, name='employee_form_update'),
    path('calendar/', views.calendar, name='calendar'),
    path('calendar/delete/<int:item_id>/', views.calendar_delete, name='calendar_delete'),
    path('calendar/<int:item_id>/', views.calendar, name='event_update'),
]
