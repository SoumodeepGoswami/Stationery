from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="goods_home"),
    path('add-good/', add_good, name="add-good"),
    path('update-good/<id>/', update_good, name="update-good"),
    path('delete-good/<id>/', delete_good, name="delete-good"),
]