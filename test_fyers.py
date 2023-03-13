from django.conf import settings
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
import json
import requests
import pandas as pd
from django.template import loader
import pytz
import schedule
import time
import pandas as pd
import datetime
import sys, os
import math
from bs4 import BeautifulSoup


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
from django.db.models import Q


# In[ ]:



APP_ID =  "TU9RDXY8QS" # App ID from myapi dashboard is in the form appId-appType. Example - EGNI8CE27Q-100, In this code EGNI8CE27Q will be APP_ID and 100 will be the APP_TYPE
APP_TYPE = "100"
SECRET_KEY = '9FL2VROLMN'
client_id= f'{APP_ID}-{APP_TYPE}'

FY_ID = "XA42364"  # Your fyers ID
APP_ID_TYPE = "2"  # Keep default as 2, It denotes web login
TOTP_KEY = "JGNW2VQHHYGGBDENCT2WEIXKJGR3CBTF"  # TOTP secret is generated when we enable 2Factor TOTP from myaccount portal
PIN = "2318"  # User pin for fyers account

REDIRECT_URI = "http://127.0.0.1:8000/api/fyers_success"  # Redirect url from the app.


# API endpoints

BASE_URL = "https://api-t2.fyers.in/vagator/v2"
BASE_URL_2 = "https://api.fyers.in/api/v2"
URL_SEND_LOGIN_OTP = BASE_URL + "/send_login_otp"   #/send_login_otp_v2
URL_VERIFY_TOTP = BASE_URL + "/verify_otp"
URL_VERIFY_PIN = BASE_URL + "/verify_pin"
URL_TOKEN = BASE_URL_2 + "/token"
URL_VALIDATE_AUTH_CODE = BASE_URL_2 + "/validate-authcode"
SUCCESS = 1
ERROR = -1

access_token=""
with open("store_token.txt","r") as outfile:
    access_token= outfile.read()

    print("access",access_token)

fyers = fyersModel.FyersModel(client_id=client_id, token= access_token)
data = {"symbols":"NSE:NIFTY50-INDEX"}
nifty_spot = fyers.quotes(data)
ans = (nifty_spot)
high_price = ans['d'][0]['v']['high_price']
low_price = ans['d'][0]['v']['low_price']
print("Nifty SPOT------------------------------------------------",nifty_spot)
print("Nifty SPOT------------------------------------------------",high_price)
print("Nifty SPOT------------------------------------------------",low_price)