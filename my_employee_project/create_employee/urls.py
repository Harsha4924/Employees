from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_employee/',views.add_employee,name="add_employee"),
    path('remove_employee/',views.remove_employee,name="remove_employee"),
    path('get_employee/',views.get_employee,name="get_employee"),
    path('submit_form/',views.submit_form,name="submit_form"),
    path('update_employee/',views.update_employee,name='update_employee'),
    path('get_all_employees/',views.get_all_employees,name='get_all_employees'),
    path('remove_employeefrom_db/',views.remove_employeefrom_db,name="remove_employeefrom_db"),
]