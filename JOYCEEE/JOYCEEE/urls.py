# JOYCEEE/urls.py
from django.contrib import admin
from django.urls import path
from contacts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.contact_list, name='contact_list'),
    path('add/', views.add_contact, name='add_contact'),
    path('update/<int:contact_id>/', views.update_contact, name='update_contact'),  # CHANGE THIS
    path('delete/<int:contact_id>/', views.delete_contact, name='delete_contact'),
]