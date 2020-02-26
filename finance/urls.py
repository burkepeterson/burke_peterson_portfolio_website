from django.urls import path
from finance import views


urlpatterns = [
    path('', views.finance_website, name='finance'),
    path('delete/<int:item_id>/', views.watchlist_delete, name='watchlist_delete'),
]
