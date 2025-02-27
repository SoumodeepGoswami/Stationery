from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='stationery_items_index'),
    path('add-item/', views.add_item, name='stationery_items_add'),
    path('update-item/<id>/', views.update_item, name='stationery_items_update'),
    path('delete-item/<id>/', views.delete_item, name='stationery_items_delete'),
]