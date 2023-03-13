# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Whatsapp_data(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=10)
    convesation_id = models.CharField(max_length=100)
    our_phone_number = models.CharField(max_length=100)
    our_phone_number_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=100)
    msg_id = models.CharField(max_length=100)
    response_from_user = models.TextField()
    message_type = models.CharField(max_length=100)
    response_from_us = models.TextField()
    New_user_check = models.BooleanField(null=True, blank=True)
    We_responded_check = models.BooleanField(null=True, blank=True)

class T_data(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=10)
    t_id = models.CharField(max_length=100)
    t_st_name = models.CharField(max_length=100)
    t_ent_price = models.FloatField()
    quantity = models.FloatField()
    proj_return = models.FloatField()
    net_return = models.FloatField()
    position_size = models.FloatField()
    type_of_t = models.CharField(max_length=100)

class ClientData(models.Model):
    status = models.CharField(max_length=10)
    remarks = models.CharField(max_length=255)
    dhanClientId = models.CharField(max_length=50)
    availableBalance = models.DecimalField(max_digits=10, decimal_places=2)
    sodLimit = models.DecimalField(max_digits=10, decimal_places=2)
    collateralAmount = models.DecimalField(max_digits=10, decimal_places=2)
    receiveableAmount = models.DecimalField(max_digits=10, decimal_places=2)
    utilizedAmount = models.DecimalField(max_digits=10, decimal_places=2)
    blockedPayoutAmount = models.DecimalField(max_digits=10, decimal_places=2)
    withdrawableBalance = models.DecimalField(max_digits=10, decimal_places=2)
class Fyer_user_profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    fy_id = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=100)

class Fyer_user_all_positions(models.Model):
    count_total = models.BigIntegerField()
    total_investment = models.DecimalField(max_digits=20, decimal_places=2)
    total_current_value = models.DecimalField(max_digits=20, decimal_places=2)
    total_pl = models.DecimalField(max_digits=20, decimal_places=2)
    pnl_perc = models.DecimalField(max_digits=20, decimal_places=2)    

class Positional_data(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=100)
    stock_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    qty = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    side = models.CharField(max_length=100)
    comments = models.TextField(blank=True)
    productType = models.CharField(max_length=100)
    trade_executed = models.BooleanField(null=True, blank=True,default=False)
    limitPrice = models.BigIntegerField(default=0,null=True, blank=True)
    stopPrice = models.BigIntegerField(default=0,null=True, blank=True)
    validity = models.CharField(max_length=100,null=True, blank=True,default="DAY")
    disclosedQty = models.BigIntegerField(max_length=100,null=True, blank=True,default=0)
    stopLoss = models.DecimalField(max_digits=10, decimal_places=2)
    takeProfit = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)

class Nifty_Data(models.Model):

    date = models.DateTimeField(auto_now_add=True, blank=True)
    entry_time = models.CharField(max_length=10)
    Nifty_entry = models.FloatField()
    Nifty_exit = models.FloatField(blank=True)
    exit_time = models.CharField(blank=True,max_length=10)
    move = models.BigIntegerField(blank=True,null=True)
    counter_nifty_data = models.CharField(max_length=10,blank=True,null=True)
    call_put = models.CharField(max_length=10,blank=True,null=True)
    Event_type = models.CharField(max_length=10,blank=True,null=True)

class Vwap_Telegram_data(models.Model):

    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=20)
    Count = models.BigIntegerField(null=True, blank=True)
    Nifty_strike = models.FloatField(null=True, blank=True)
    entry_price = models.FloatField(null=True, blank=True)
    exit_price = models.FloatField(null=True, blank=True)
    TV_candle_conf_red = models.BooleanField(null=True, blank=True)
    TV_candle_conf_green = models.BooleanField(null=True, blank=True)
    TV_candle_exit_2_red = models.BooleanField(null=True, blank=True)
    TV_candle_exit_2_green = models.BooleanField(null=True, blank=True)
    TV_exit_70_25_rsi = models.BooleanField(null=True, blank=True)
    TV_exit_rsi_cross_down = models.BooleanField(null=True, blank=True)
    type_of_option =models.CharField(max_length=10,null=True, blank=True)
    net_point_captured = models.FloatField(null=True, blank=True)


