# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    # The home page
    path('adminkitchen', views.index, name='home'),
    path('login_adminkitchen', views.login_adminkitchen),
    path('logout_adminkitchen', views.logout_adminkitchen, name="logout"),
    path('kitchen_adminview', views.kitchen_adminview),
    path('category_list', views.category_list),
    path('category_edit/<int:pk>', views.category_edit),
    path('kitchen_location', views.kitchen_location)
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
    # path("logout_adminkitchen", LogoutView.as_view(), name="logout")

]
