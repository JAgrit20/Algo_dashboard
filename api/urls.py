from django.urls import path
from . import views

urlpatterns = [
	path('', views.apiOverview, name="api-overview"),
	path('task-list/', views.taskList, name="task-list"),
	path('task-detail/<str:pk>/', views.taskDetail, name="task-detail"),


	path('task-create/', views.taskCreate_data, name="task-create"),
	path('task-create_5min/', views.taskCreate_data_5min, name="task-create_5min"),
	path('task-create_stocastic_up/', views.taskCreate_data_stocastic_up, name="task-create_stocastic_up"),
	path('task-create_stocastic_ADX/', views.taskCreate_data_stocastic_ADX, name="task-create_stocastic_ADX"),

	path('task-create_stocastic_up_DXY/', views.taskCreate_data_stocastic_up_DXY, name="task-create_stocastic_up_DXY"),
	path('task-create_stocastic_ADX_DXY/', views.taskCreate_data_stocastic_ADX_DXY, name="task-create_stocastic_ADX_DXY"),
	
	path('task-create_adx/', views.taskCreate_adx, name="task-create_adx"),
	path('task-create_rsi/', views.taskCreate_RSI, name="task-create_rsi"),
	path('taskCreate_ADX_5min/', views.taskCreate_ADX_5min, name="taskCreate_ADX_5min/"),

	path('task-create_nifty_buy/', views.Nifty_Create_buy, name="task-create_nifty"),
	path('task-create_nifty_sell/', views.Nifty_Create_sell, name="task-create_nifty"),
	path('task-create_nifty_exit/', views.Nifty_Create_exit, name="task-create_nifty"),
	path('task-update_nifty/', views.Nifty_Update, name="task-update_nifty"),
	path('task-update_nifty_exit/', views.Nifty_Create_exit, name="task-update_nifty_exit"),
	path('task-update/<str:pk>/', views.taskUpdate, name="task-update"),
	path('task-delete/<str:pk>/', views.taskDelete, name="task-delete"),


    path('green_candle_conf/', views.green_candle_conf, name="green_candle_conf"),
	path('red_candle_conf/', views.red_candle_conf, name="red_candle_conf"),

    path('consicutive_green_candle/', views.consicutive_green_candle, name="green_candle_conf"),
	path('consicutive_red_candle/', views.consicutive_red_candle, name="red_candle_conf"),
    path('TV_exit_70_25_rsi/', views.TV_exit_70_25_rsi, name="green_candle_conf"),
	path('TV_exit_rsi_cross_down/', views.TV_exit_rsi_cross_down, name="red_candle_conf"),
]
