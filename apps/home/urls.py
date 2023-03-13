# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('/get_portfolio', views.Get_portfolio, name='Get_portfolio'),
    path('save_positional_stock',views.save_positional_stock,name='save_positional_stock'),
    path('add-stock',views.addstock,name='add-stock'),
    path('vwap_data',views.vwap_data,name='vwap_data'),
    path('DXY',views.DXY,name='DXY'),

    # path('vwap_data',views.vwap_data,name='vwap_data'),

 
	# path('task-create_stocastic_up/', views.taskCreate_data_stocastic_up, name="task-create_stocastic_up"),
	# path('task-create_stocastic_ADX/', views.taskCreate_data_stocastic_ADX, name="task-create_stocastic_ADX"),


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
