from django.conf import settings
from django.shortcuts import render, get_object_or_404
# from counter.models import Counter, PCR_data, PCR_data_past,BTC_Data
from django.http import HttpResponse
import json
import requests
from bs4 import BeautifulSoup

from django.template import loader
import datetime as dt
import datetime
import pytz
# import schedule
import time
import datetime
import sys, os

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

	print("Telegram_data add")
	dtobj1 = datetime.datetime.utcnow()  # utcnow class method
	stockcode = ['ADANIENT', 'ADANIPORTS', 'APOLLOHOSP', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BPCL', 'BHARTIARTL', 'BRITANNIA', 'CIPLA', 'COALINDIA', 'DIVISLAB', 'DRREDDY', 'EICHERMOT', 'GRASIM', 'HCLTECH', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO',
				 'HINDUNILVR', 'HDFC', 'ICICIBANK', 'ITC', 'INDUSINDBK', 'INFY', 'JSWSTEEL', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NTPC', 'NESTLEIND', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBILIFE', 'SBIN', 'SUNPHARMA', 'TCS', 'TATACONSUM', 'TATAMOTORS', 'TATASTEEL', 'TECHM', 'TITAN', 'UPL', 'ULTRACEMCO', 'WIPRO']
	# print(stockcode)
	url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'

	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9'
	}
	response = requests.get(url, headers=headers).content
	data = json.loads(response)
	nifty_val = 0
	count = 0
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

	print("count", count)
	if(count >= 40):
		Send_high()
	if(count <= 10):
		Send_low()
	# counter = counter + 1
	# print(counter)
	# dtobj1 = datetime.datetime.utcnow()  # utcnow class method

	# 	# print(dtobj1)
	# dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)  # replace method

		# print(pytz.all_timezones) => To see all timezones
	# dtobj_india = dtobj3.astimezone(pytz.timezone("Asia/Calcutta"))  # astimezone method
	# print("India time data_add", dtobj_india)
	# dtobj_india = dtobj_india.strftime("%H:%M")
	# dtobj_indiaa = str(dtobj_india)
	# # datetime_ist = datetime.now(IST)
	# # print(datetime_ist.strftime('%Y:%m:%d %H:%M:%S %Z %z'))
	# ans = Telegram_data.objects.latest('id')
	# nift_prev = ans['Nifty_new']
	# Telegram_data_entry = Telegram_data(time=dtobj_indiaa,Nifty_prev=nift_prev,Nifty_new= nifty_val,Count=count)
	# Telegram_data_entry2 = PCR_data_past(time=dtobj_indiaa, call=tol_CE_vol, put=tol_PE_vol, pcrOI=pcrOI, diffOI=diffOI,
	# 									 diff=diff, pcr=pcr, price=nifty_val, option_signal=signal, callOI=totCE, putOI=totPE)

Telegram_data()