from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('employee/', include('employee_management.urls')),
    path('finance/', include('finance.urls')),
    path('accounts/', include('allauth.urls')),
]
