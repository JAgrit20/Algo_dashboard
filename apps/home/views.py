# -*- encoding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Positional_data
from rest_framework.exceptions import AuthenticationFailed
from django.views.decorators.csrf import csrf_exempt
from . models import ClientData,Fyer_user_profile,Fyer_user_all_positions,Vwap_Telegram_data,DXY_RSI_60
from django.contrib import messages
# from users.models import Bookmark, Personalisation, User
# from users.api.serializers import BookmarkSerializer, UserSerializer, PersonalisationSerializer
import jwt, datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
import pytz
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime as dt
import datetime
import pytz
import schedule
import time
import math
import json
import requests
import pandas as pd
from fyers_api import fyersModel
import json


from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# from .models import Counter, PCR_data,Telegram_data,BTC_Data,Nifty_Data,Stocastic_Data,Stocastic_Data_DXY

import json
import requests
import time
import pyotp
import os
import requests
from urllib.parse import parse_qs,urlparse
import sys
from fyers_api import fyersModel
from fyers_api import accessToken


APP_ID =  "TU9RDXY8QS" # App ID from myapi dashboard is in the form appId-appType. Example - EGNI8CE27Q-100, In this code EGNI8CE27Q will be APP_ID and 100 will be the APP_TYPE
APP_TYPE = "100"
SECRET_KEY = '9FL2VROLMN'
client_id= f'{APP_ID}-{APP_TYPE}'

@login_required(login_url="/login/")
def index(request):

    # filtered_rows = MyModel.objects.filter(field_name=value)

    # row_count = filtered_rows.count()

    
    Positional_data_count = Positional_data.objects.count()


    try:
        with open("store_token.txt","r") as outfile:
            access_token= outfile.read()
            print("access",access_token)
        # print(get_access_token())
        fyers = fyersModel.FyersModel(client_id=client_id, token= access_token)
        # symbol = {'symbols': 'NSE:TATAMOTORS-EQ'}
        # print(fyers.quotes(symbol))
        all_user_data = fyers.get_profile()

        fid = (all_user_data['data']['fy_id'])
        name = (all_user_data['data']['name'])
        email = (all_user_data['data']['email_id'])
        mob = (all_user_data['data']['mobile_number'])

        fyer_user_profile = Fyer_user_profile(fy_id= fid, name = name, email = email, mobile_no = mob)
        fyer_user_profile.save()

        all_post_data = fyers.holdings()

        count_total = all_post_data['overall']['count_total']
        total_investment = all_post_data['overall']['total_investment']
        total_current_value = all_post_data['overall']['total_current_value']
        total_pl = all_post_data['overall']['total_pl']
        pnl_perc = all_post_data['overall']['pnl_perc']

        all_post_data = Fyer_user_all_positions(count_total=count_total,total_investment=total_investment,total_current_value=total_current_value,total_pl=total_pl,pnl_perc=pnl_perc)
        all_post_data.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
    latest_client_data = Fyer_user_profile.objects.order_by('-pk').first()
    latest_post_data = Fyer_user_all_positions.objects.order_by('-pk').first()
    print("--------------------------------------------------------------------")
    print(latest_client_data)
    all_posti_stocks = Positional_data.objects.filter(trade_executed=False).order_by('-date_time')[:5]
    all_posti_stocks_all = Positional_data.objects.order_by('-date_time')
    
    context = {'segment': 'index','latest_client_data':latest_client_data,'latest_post_data':latest_post_data,'all_posti_stocks_all':all_posti_stocks_all ,'all_posti_stocks':all_posti_stocks,'Positional_data_count':Positional_data_count}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@csrf_exempt
def save_positional_stock(request):

    dtobj1 = datetime.datetime.utcnow()  # utcnow class method
    dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method
    dtobj_india = dtobj3.astimezone(pytz.timezone("Asia/Calcutta"))  # astimezone method
    print("India time data_add", dtobj_india)
    dtobj_india = dtobj_india.strftime("%Y-%m-%d %H:%M")
    dtobj_indiaa = str(dtobj_india)
    context = {}
    if request.method=='POST':
        limitPrice =0
        stopPrice =0
        disclosedQty =0
        stopLoss =0
        takeProfit =0

        symbol=request.POST['symbol']
        Order_Type=request.POST['Order_Type']
        Stock_Name=request.POST['Stock_Name']
        qty=request.POST['qty']
        side=request.POST['side']
        productType=request.POST['productType']
        if request.POST['limitPrice']:
            limitPrice=request.POST['limitPrice']
        if request.POST['stopPrice']:
            stopPrice=request.POST['stopPrice']
        validity=request.POST['validity']
        if request.POST['disclosedQty']:
            disclosedQty=request.POST['disclosedQty']
        if request.POST['stopLoss']:
            stopLoss=request.POST['stopLoss']
        if request.POST['takeProfit']:
            takeProfit=request.POST['takeProfit']

        exchange=request.POST['exchange']

        print("Symbol:", symbol)
        print("Order Type:", Order_Type)
        print("Stock Name:", Stock_Name)
        print("Quantity:", qty)
        print("Side:", side)
        print("Product Type:", productType)
        print("Limit Price:", limitPrice)
        print("Stop Price:", stopPrice)
        print("Validity:", validity)
        print("Disclosed Quantity:", disclosedQty)
        print("Stop Loss:", stopLoss)
        print("Take Profit:", takeProfit)
        print(" exchange:", exchange)

        if(exchange=="nse_eq"):
            symbol = "NSE:"+symbol+"-EQ"
        if(exchange=="bse_eq"):
            symbol = "BSE:"+symbol+"-EQ"
            print("nse")
        try:
            pos_data_entry = Positional_data(time=dtobj_indiaa,symbol=symbol,stock_name=Stock_Name,qty=qty,type=Order_Type,side=side,productType= productType,limitPrice= limitPrice,stopPrice=stopPrice,validity=validity,disclosedQty=disclosedQty,stopLoss=stopLoss,takeProfit=takeProfit)
            ans = pos_data_entry.save()
            messages.success(request, 'Stock Added for monitoring')
            print("meesage sent")
        except:
            messages.error(request, 'Failed to Add, Message Jagrit')

        print(Order_Type)
        print(Stock_Name)
        last_obj = Positional_data.objects.last()
        context = {"last_obj":last_obj}
        html_template = loader.get_template('home/add-stock.html')
        return HttpResponse(html_template.render(context, request))
@csrf_exempt
def addstock(request):
    last_obj = Positional_data.objects.last()
    context = {"last_obj":last_obj}
    html_template = loader.get_template('home/add-stock.html')
    return HttpResponse(html_template.render(context, request))
@csrf_exempt
def vwap_data(request):
    latest_post_data = Vwap_Telegram_data.objects.order_by('-pk')

    context = {"last_obj":latest_post_data}
    html_template = loader.get_template('home/vwap_data_record.html')
    return HttpResponse(html_template.render(context, request))
@csrf_exempt
def dxy(request):
    latest_post_data = DXY_RSI_60.objects.order_by('-pk')

    context = {"last_obj":latest_post_data}
    html_template = loader.get_template('home/DXY_data_record.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@api_view(['GET'])
def Get_portfolio(request):

    client_data = ClientData(status=data_dict['status'],
                            remarks=data_dict['remarks'],
                            dhanClientId=data_dict['data']['dhanClientId'],
                            availableBalance=data_dict['data']['availableBalance'],
                            sodLimit=data_dict['data']['sodLimit'],
                            collateralAmount=data_dict['data']['collateralAmount'],
                            receiveableAmount=data_dict['data']['receiveableAmount'],
                            utilizedAmount=data_dict['data']['utilizedAmount'],
                            blockedPayoutAmount=data_dict['data']['blockedPayoutAmount'],
                            withdrawableBalance=data_dict['data']['withdrawableBalance'])

    client_data.save()
    return Response(serializer.data)
