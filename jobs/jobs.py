from django.conf import settings
from django.shortcuts import render, get_object_or_404
from apps.home.models import Vwap_Telegram_data
from django.http import HttpResponse
import json
import requests
import pandas as pd
from django.template import loader
import datetime as dt
import datetime
import pytz
import schedule
import time
import pandas as pd
import datetime
import sys, os
import math
from bs4 import BeautifulSoup
from apps.home.models import Positional_data


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

def strategy_5():

    print("Running VWAP")

    print("Telegram_data add")
    dtobj1 = datetime.datetime.utcnow()  # utcnow class method
    stockcode = ['ADANIENT', 'ADANIPORTS', 'APOLLOHOSP', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BPCL', 'BHARTIARTL', 'BRITANNIA', 'CIPLA', 'COALINDIA', 'DIVISLAB', 'DRREDDY', 'EICHERMOT', 'GRASIM', 'HCLTECH', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO',
                 'HINDUNILVR', 'HDFC', 'ICICIBANK', 'ITC', 'INDUSINDBK', 'INFY', 'JSWSTEEL', 'KOTAKBANK', 'LT', 'M%26M', 'MARUTI', 'NTPC', 'NESTLEIND', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBILIFE', 'SBIN', 'SUNPHARMA', 'TCS', 'TATACONSUM', 'TATAMOTORS', 'TATASTEEL', 'TECHM', 'TITAN', 'UPL', 'ULTRACEMCO', 'WIPRO']
    # print(stockcode)
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    response = requests.get(url, headers=headers).content
    data = json.loads(response)
    count = 0
    nifty_val = 0
    nifty_val = data['filtered']['data'][0]['PE']['underlyingValue']
    print("nifty_val", nifty_val)

    for i in range(len(stockcode)):
            try:
                stock_url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=' + \
                    str(stockcode[i])
                print(stock_url)
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
                response = requests.get(stock_url, headers=headers)
                # response
                soup = BeautifulSoup(response.text, 'html.parser')
                data_array = soup.find(id='responseDiv').getText()

                y = json.loads(data_array)

                latest_price = (y['data'][-1]['lastPrice'])
                latest_price = latest_price.replace(',', '')
                print("latest", latest_price)
                latest_price = float(latest_price)

                # name = "SUNPHARMA"

                url = f'https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={stockcode[i]}&smeFlag=0&itpFlag=0'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}

                soup = BeautifulSoup(requests.get(
                    url, headers=headers).content, 'html.parser')
                data = json.loads(soup.select_one('#responseDiv').text)

                # uncomment this to print all data:
                # print(json.dumps(data, indent=4))
                vwap = (data['data'][0]['averagePrice'])
                vwap = vwap.replace(',', '')
                vwap = float(vwap)
                # print("v",type(vwap))
                # print("latest_price",type(latest_price))
                vwap = float(vwap)

                print('vwap:', data['data'][0]['averagePrice'])

                if(latest_price > vwap):
                    count = count + 1
                # print("yes big")
                # else:
                #   # print("small")
            except Exception as e:
                print("ERROR : "+str(e))
    
    dtobj1 = datetime.datetime.utcnow()  # utcnow class method
    dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method
    dtobj_india = dtobj3.astimezone(pytz.timezone("Asia/Calcutta"))  # astimezone method
    print("India time data_add", dtobj_india)
    dtobj_india = dtobj_india.strftime("%H:%M:%S")
    dtobj_indiaa = str(dtobj_india)
    print("count", count)
    field_value_signal = 0
    try:
        field_name = 'Nifty_strike'
        obj = Vwap_Telegram_data.objects.last()
        field_value_signal = getattr(obj, field_name)
    except:
        pass
    if(count > 40):
        
        prev_spot = field_value_signal
        spot = float(nifty_val)
        b = float(spot/100)
        b = float(b)
        c = math.floor(b)
        d = float((c+0.5 )*100)
        e = float((c-0.5 )*100)
        d= int(d)
        e= int(e)
        Telegram_data_entry = Vwap_Telegram_data(time=dtobj_indiaa,Nifty_strike=nifty_val,entry_price= d,exit_price=0,Count=count,type_of_option="PUT",net_point_captured=prev_spot-spot)
        # Send_high()
        Telegram_data_entry.save()
        access_token=""
        with open("store_token.txt","r") as outfile:
            access_token= outfile.read()

            print("access",access_token)
            
        fyers = fyersModel.FyersModel(client_id=client_id, token= access_token)
        data = {
        "symbol":f"NSE:NIFTY23309{e}PE",
        "qty":50,
        "type":2,
        "side":1,
        "productType":"INTRADAY",
        "limitPrice":0,
        "stopPrice":0,
        "validity":"DAY",
        "disclosedQty":0,
        "offlineOrder":"False",
        "stopLoss":0,
        "takeProfit":0
        }
        print(f"NSE:NlFTY23309{d}PE")

        order_data = fyers.place_order(data)
        print(order_data)
     

    if(count <= 10):
        prev_spot = field_value_signal
        spot = float(nifty_val)
        b = float(spot/100)
        b = float(b)
        c = math.floor(b)
        d = float((c+0.5 )*100)
        e = float((c-0.5 )*100)
        d= int(d)
        e= int(e)
        Telegram_data_entry = Vwap_Telegram_data(time=dtobj_indiaa,Nifty_strike=nifty_val,entry_price= e,exit_price=0,Count=count,type_of_option="CALL",net_point_captured=prev_spot-spot)
        # Send_low()
        Telegram_data_entry.save()
        access_token=""
        with open("store_token.txt","r") as outfile:
            access_token= outfile.read()
            print("access",access_token)
        fyers = fyersModel.FyersModel(client_id=client_id, token= access_token)
        data = {
        "symbol":f"NSE:NlFTY23309{d}CE",
        "qty":1,
        "type":2,
        "side":1,
        "productType":"INTRADAY",
        "limitPrice":0,
        "stopPrice":0,
        "validity":"DAY",
        "disclosedQty":0,
        "offlineOrder":"False",
        "stopLoss":0,
        "takeProfit":0
        }
        print(f"NSE:NlFTY23309{d}CE")

        order_data = fyers.place_order(data)
        print(order_data)


def send_login_otp(fy_id, app_id):
    try:
        result_string = requests.post(url=URL_SEND_LOGIN_OTP, json= {"fy_id": fy_id, "app_id": app_id })
        if result_string.status_code != 200:
            return [ERROR, result_string.text]
        result = json.loads(result_string.text)
        request_key = result["request_key"]
        return [SUCCESS, request_key]
    except Exception as e:
        return [ERROR, e]

def verify_totp(request_key, totp):
    try:
        result_string = requests.post(url=URL_VERIFY_TOTP, json={"request_key": request_key,"otp": totp})
        if result_string.status_code != 200:
            return [ERROR, result_string.text]
        result = json.loads(result_string.text)
        request_key = result["request_key"]
        return [SUCCESS, request_key]
    except Exception as e:
        return [ERROR, e]


def get_access_token():
    # if not os.path.exists("store_token.txt"):
    session = accessToken.SessionModel(client_id=client_id, secret_key=SECRET_KEY, redirect_uri=REDIRECT_URI,
                                response_type='code', grant_type='authorization_code')

    urlToActivate = session.generate_authcode()
    print(f'URL to activate APP:  {urlToActivate}')



    # Step 1 - Retrieve request_key from send_login_otp API

    send_otp_result = send_login_otp(fy_id=FY_ID, app_id=APP_ID_TYPE)

    if send_otp_result[0] != SUCCESS:
        print(f"send_login_otp failure - {send_otp_result[1]}")
        sys.exit()
    else:
        print("send_login_otp success")


    # Step 2 - Verify totp and get request key from verify_otp API
    for i in range(1,3):
        request_key = send_otp_result[1]
        verify_totp_result = verify_totp(request_key=request_key, totp=pyotp.TOTP(TOTP_KEY).now())
        if verify_totp_result[0] != SUCCESS:
            print(f"verify_totp_result failure - {verify_totp_result[1]}")
            time.sleep(1)
        else:
            print(f"verify_totp_result success {verify_totp_result}")
            break

    request_key_2 = verify_totp_result[1]

    # Step 3 - Verify pin and send back access token
    ses = requests.Session()
    payload_pin = {"request_key":f"{request_key_2}","identity_type":"pin","identifier":f"{PIN}","recaptcha_token":""}
    res_pin = ses.post('https://api-t2.fyers.in/vagator/v2/verify_pin', json=payload_pin).json()
    print(res_pin['data'])
    ses.headers.update({
        'authorization': f"Bearer {res_pin['data']['access_token']}"
    })



    authParam = {"fyers_id":FY_ID,"app_id":APP_ID,"redirect_uri":REDIRECT_URI,"appType":APP_TYPE,"code_challenge":"","state":"None","scope":"","nonce":"","response_type":"code","create_cookie":True}
    authres = ses.post('https://api.fyers.in/api/v2/token', json=authParam).json()
    # print("autheres",authres)
    url = authres['Url']
    # print(url)
    parsed = urlparse(url)
    auth_code = parse_qs(parsed.query)['auth_code'][0]



    session.set_token(auth_code)
    response = session.generate_token()
    # print("REs", response)
    access_token= response["access_token"]
    # print(access_token)
    with open("store_token.txt","w") as outfile:
        outfile.write(access_token)
    # else:
    #     with open("store_token.txt","r") as outfile:
    #         access_token= outfile.read()
            # print("access",token_response)
    return access_token 

# Get profile name


def update_token():
    # print(get_access_token())
    fyers = fyersModel.FyersModel(client_id=client_id, token= get_access_token())
    # symbol = {'symbols': 'NSE:TATAMOTORS-EQ'}
    # print(fyers.quotes(symbol))
    all_user_data = fyers.get_profile()
    print(all_user_data['data']['fy_id'])
    print(all_user_data['data']['name'])
    print(all_user_data['data']['email_id'])
    print(all_user_data['data']['mobile_number'])

def Place_positional_order():
    with open("store_token.txt","r") as outfile:
        access_token= outfile.read()
        print("access",access_token)
    # print(get_access_token())
    fyers = fyersModel.FyersModel(client_id=client_id, token= access_token)
    all_posti_stocks = Positional_data.objects.filter(trade_executed=False).order_by('-date_time')[:5]
    # symbol = {'symbols': 'NSE:TATAMOTORS-EQ'}
    # print(fyers.quotes(symbol))
    for i in all_posti_stocks:
        print(i.qty)
        data = {
            "symbol":i.symbol,
            "qty":int(i.qty),
            "type":int(i.type),
            "side":int(i.side),
            "productType":i.productType,
            "limitPrice":int(i.limitPrice),
            "stopPrice":int(i.stopPrice),
            "validity":i.validity,
            "disclosedQty":int(i.disclosedQty),
            "offlineOrder":"False",
            "stopLoss":int(i.stopLoss),
            "takeProfit":int(i.takeProfit)
            }

        resp = fyers.place_order(data)
        print(resp)




def Send_high():
    import requests
    import json

    url = "https://api.telegram.org/bot5820846301%3AAAHYbFAlHnqDfzbHFPZHdO1O1u6Y21UJzVg/sendMessage"

    payload = {
        "text": "Count is more than 40",
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": None,
        "chat_id": "-1001691472772"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


# In[5]:
# Send_high()

def Send_low():
    import requests
    import json

    url = "https://api.telegram.org/bot5921643018:AAHmiFfQudRMNZNl3sG19zafMZD0OdfWGgA/sendMessage"

    payload = {
        "text": "Count is less than 10",
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": None,
        "chat_id": "-1001691472772"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


def Telegram_data():
    print("data added PUT")


def schedule_api():
    try:
        print("Schdule API")
        dtobj1 = datetime.datetime.utcnow()  # utcnow class method

        # print(dtobj1)
        dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method

        # print(pytz.all_timezones) => To see all timezones
        dtobj_india = dtobj3.astimezone(
            pytz.timezone("Asia/Calcutta"))  # astimezone method
        print("India time data_add", dtobj_india)

        url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9'
        }
        response = requests.get(url, headers=headers).content
        data = json.loads(response.decode('utf-8'))

        expiry_dt = data['records']['expiryDates'][0]
        new_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'

        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(new_url, headers=headers)
        dajs = json.loads(page.text)

        ce_values = [data['CE'] for data in dajs['records']['data']
                     if "CE" in data and data['expiryDate'] == expiry_dt]
        pe_values = [data['PE'] for data in dajs['records']['data']
                     if "PE" in data and data['expiryDate'] == expiry_dt]
        ce_dt = pd.DataFrame(ce_values).sort_values(['strikePrice'])

        pe_dt = pd.DataFrame(pe_values).sort_values(['strikePrice'])

        print(ce_dt.columns.tolist())

        totCE = ce_dt['openInterest'].sum()
        print("openInterest", totCE)
        tol_CE_vol = ce_dt['totalTradedVolume'].sum()
        print("totalTradedVolume", tol_CE_vol)
        totPE = pe_dt['openInterest'].sum()
        print("openInterest", totPE)
        tol_PE_vol = pe_dt['totalTradedVolume'].sum()
        print("totalTradedVolume", tol_PE_vol)

        # totCE = data['filtered']['CE']['totOI']
        totc = data['filtered']['CE']
        totp = data['filtered']['CE']
        # totPE = data['filtered']['PE']['totOI']
        # tol_PE_vol = data['filtered']['PE']['totVol']
        # tol_CE_vol = data['filtered']['CE']['totVol']
        nifty_val = 0
        nifty_val = data['filtered']['data'][0]['PE']['underlyingValue']
        dtobj_india = dtobj_india.strftime("%H:%M:%S")
        dtobj_indiaa = str(dtobj_india)

        diff = tol_CE_vol - tol_PE_vol

        diffOI = totCE - totPE

        pcr = tol_PE_vol/tol_CE_vol
        pcrOI = totPE/totCE

        print("PCR", pcr)
        signal = "BUY"
        if(pcr > 1):
            signal = "BUY"
        else:
            signal = "SELL"

        pcr_data_entry = PCR_data(time=dtobj_indiaa, call=tol_CE_vol, put=tol_PE_vol, pcrOI=pcrOI, diffOI=diffOI,
                                  diff=diff, pcr=pcr, price=nifty_val, option_signal=signal, callOI=totCE, putOI=totPE)
        pcr_data_entry2 = PCR_data_past(time=dtobj_indiaa, call=tol_CE_vol, put=tol_PE_vol, pcrOI=pcrOI, diffOI=diffOI,
                                        diff=diff, pcr=pcr, price=nifty_val, option_signal=signal, callOI=totCE, putOI=totPE)

        ans = pcr_data_entry.save()
        ans1 = pcr_data_entry2.save()
        print("saving data")
        # print("ans", ans)

    except Exception as e:
        print("something went wrong", e)

        # 77779

# def getting_btc_data_past():
# 	try:
# 		# print("getting_btc_data")
# 		dtobj1 = datetime.datetime.utcnow()  # utcnow class method

# 		# print(dtobj1)
# 		dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method

# 		# print(pytz.all_timezones) => To see all timezones
# 		dtobj_india = dtobj3.astimezone(
# 			pytz.timezone("Asia/Calcutta"))  # astimezone method
# 		print("India time data_add", dtobj_india)

# 		url = 'https://api.taapi.io/rsi?secret=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjNiZGQyZjRmYzVhOGFkZmVjOWE4YmY2IiwiaWF0IjoxNjczMzg0NjkyLCJleHAiOjMzMTc3ODQ4NjkyfQ.EdXPuHkbcD1G024Pk9Ml0zTzhSfd2Ptbvueyor1Ifw0&exchange=binance&symbol=BTC/USDT&interval=1m'

# 		headers = {
# 			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
# 			'accept-encoding': 'gzip, deflate, br',
# 			# 'accept-language': 'en-US,en;q=0.9'
# 		}
# 		sma = 0
# 		response = requests.get(url, headers=headers).content
# 		data = json.loads(response.decode('utf-8'))
# 		# print("Data2",data)
# 		print("Data",data)
# 		rsi = float(data['value'])	

# 		dtobj_india = dtobj_india.strftime("%H:%M:%S")

# 		dtobj_indiaa = str(dtobj_india)
# # Add indicators, using data from before
# 		mydata = BTC_Data.objects.all().values()
# 		df = pd.DataFrame(list(BTC_Data.objects.all().order_by('id').values()))


# 		#Create a simple moving average with a 30 day window
# 		# SMA_30_pd = SMA_30_pd.DataFrame()('Adj Close').rolling(window=30).mean()

# 		df.ta.sma(close='RSI', length=7, append=True)


# 		# df.ta.sma(close='RSI', length=20, append=True)
        
# 		json_records = df.reset_index().to_json(orient ='records')
# 		data = []
# 		data = json.loads(json_records)
# 		# print("dfff",df)
# 		# print(df.tail(15))
# 		# print(df['SMA_7'].loc[df.index[-1]])
# 		sma =0


# 		field_name_signal = 'signal'
# 		field_name_price = 'price'

# 		obj = BTC_Data.objects.last()

# 		field_value_signal = getattr(obj, field_name_signal)
# 		field_value_price = getattr(obj, field_name_price)

# 		pcr_data_entry = BTC_Data(time=dtobj_indiaa, RSI=rsi,SMA=sma,price=field_value_price, signal=field_value_signal)

# 		ans = pcr_data_entry.save()
# 		print("saving data")
# 		# print("ans", ans)

# 	except Exception as e:
# 		exc_type, exc_obj, exc_tb = sys.exc_info()
# 		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
# 		print(exc_type, fname, exc_tb.tb_lineno)
# 		print("something went wrong", e) 

        # 77779
def getting_btc_data():
    try:
        # print("getting_btc_data")
        dtobj1 = datetime.datetime.utcnow()  # utcnow class method

        # print(dtobj1)
        dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method

        # print(pytz.all_timezones) => To see all timezones
        dtobj_india = dtobj3.astimezone(
            pytz.timezone("Asia/Calcutta"))  # astimezone method
        print("India time data_add", dtobj_india)

        # print("Data2",data)
        dtobj_india = dtobj_india.strftime("%H:%M:%S")

        dtobj_indiaa = str(dtobj_india)

        field_name_signal = 'signal'
        field_name_price = 'price'
        field_name_rsi = 'RSI'
        field_name_sma = 'SMA'
        field_name_adx = 'signal_adx'
        field_name_signal_5min= 'signal_5min'

        field_name_price_5min= 'price_5min'
        field_name_signal_adx_5min= 'signal_adx_5min'
        obj = BTC_Data.objects.last()
        # print("obj", obj)
        field_value_signal = getattr(obj, field_name_signal)
        field_value_price = getattr(obj, field_name_price)
        field_value_rsi = getattr(obj, field_name_rsi)
        field_value_sma = getattr(obj, field_name_sma)
        field_value_adx = getattr(obj, field_name_adx)
        field_value_5min = getattr(obj, field_name_signal_5min)
        field_value_5min_p = getattr(obj, field_name_price_5min)
        field_value_5min_adx = getattr(obj, field_name_signal_adx_5min)

        pcr_data_entry = BTC_Data(time=dtobj_indiaa, RSI=field_value_rsi,SMA=field_value_sma,price=field_value_price, signal=field_value_signal,signal_adx = field_value_adx,signal_5min = field_value_5min,price_5min=field_value_5min_p,signal_adx_5min=field_value_5min_adx)

        ans = pcr_data_entry.save()
        print("saving data")
        # print("ans", ans)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print("something went wrong", e) 

        # 77779
