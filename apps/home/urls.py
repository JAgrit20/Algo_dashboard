
from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('/get_portfolio', views.Get_portfolio, name='Get_portfolio'),
    path('save_positional_stock',views.save_positional_stock,name='save_positional_stock'),
    path('add-stock',views.addstock,name='add-stock'),
    path('vwap_data',views.vwap_data,name='vwap_data'),
    path('dxy',views.dxy,name='dxy'),
    path('check_dxy_rsi_60', views.check_dxy_rsi_60, name='check_dxy_rsi_60'),
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
