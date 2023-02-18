# -*- encoding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from . models import ClientData
# from users.models import Bookmark, Personalisation, User
# from users.api.serializers import BookmarkSerializer, UserSerializer, PersonalisationSerializer
import jwt, datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# from .models import Counter, PCR_data,Telegram_data,BTC_Data,Nifty_Data,Stocastic_Data,Stocastic_Data_DXY

from dhanhq import dhanhq

cleintid = '1100082542'
accessToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNjc5MTE3NjIyLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJkaGFuQ2xpZW50SWQiOiIxMTAwMDgyNTQyIn0.WxEaNAzJxz-ogfOotKST82wk0BjZiNsi-nUnQZbk_djd0iJ_R04Y-cuPw4rLJyixJ7kdxLg1ivj5e8f3ScqmDg'

dhan = dhanhq(cleintid,accessToken)
@login_required(login_url="/login/")
def index(request):

    try:
        data_dict = dhan.get_fund_limits()
        print(data_dict)
        client_data = ClientData(status=data_dict['status'],
                                remarks=data_dict['remarks'],
                                dhanClientId=data_dict['data']['dhanClientId'],
                                availableBalance=data_dict['data']['availabelBalance'],
                                sodLimit=data_dict['data']['sodLimit'],
                                collateralAmount=data_dict['data']['collateralAmount'],
                                receiveableAmount=data_dict['data']['receiveableAmount'],
                                utilizedAmount=data_dict['data']['utilizedAmount'],
                                blockedPayoutAmount=data_dict['data']['blockedPayoutAmount'],
                                withdrawableBalance=data_dict['data']['withdrawableBalance'])

        client_data.save()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
    latest_client_data = ClientData.objects.order_by('-pk').first()
    print("--------------------------------------------------------------------")
    print(latest_client_data)
    
    context = {'segment': 'index','latest_client_data':latest_client_data}
    html_template = loader.get_template('home/index.html')
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

