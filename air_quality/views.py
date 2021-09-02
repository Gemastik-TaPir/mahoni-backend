from django.http.response import HttpResponse
from django.shortcuts import render
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timezone

from air_quality.models import Air_quality
from air_quality.serializers import Air_QualitySerialization
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Create your views here.
headers_dict = {"Accept": "application/json","apikey":"kztKksBBnM6j4CzEb0FKu546eZG4lnym"}

url = "https://airapi.airly.eu/v2/measurements/installation?installationId="
'''
id_location = [37913,36785,36154,80753,37936,80688,33037,18441,18471,16741,37096,18434,39774,
    36081,18499,40885,18442,36118,18484,41029,18467,32995,35829,80763,18456,14266,80765,38596,35831,
    40905,16692,33065,35758,38597,41245,18483,42394,18455,36063,18450,43771,80689,18439,18583,36067,
    43353,35754,35291,18693,43352,38594,38595,43351,80686,18541,14273,32994,80832,33056,36937,40886,
    36936,16691,13124,33041,40882,33055,33066,35755,36065,80757,80640,18540,35787,16689,33064,80693,
    18453,35960,42975,82297,41247,35753,18497]
'''
id_location = [37913,36785]

yesterday = np.array([['-','','',0,0,0,0]]*2016)
tomorrow = np.array([['-','','',0,0,0]]*2016)
current = np.array([['-','','',0,0,0,0]]*84)
def test(request):
    return HttpResponse('test')

def get_air_quality(request):
    print('no')
    count = 0
    for id in id_location :
        print('yes')
        resp = requests.get(url+str(id), headers=headers_dict).json()
        get_current(resp,count,id)
        print('yes')
        #get_past(resp,count*24,id)
        #get_future(resp,count*24,id)
        count+=1
    return HttpResponse('done')
    

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def get_current(resp,count,id):
    
    global current
    try:
        date_now_from_json = resp['current'].get("tillDateTime")
        date_now = utc_to_local(datetime.strptime(date_now_from_json,'%Y-%m-%dT%H:%M:%S.%fZ')).strftime("%Y-%m-%d")
        time = utc_to_local(datetime.strptime(date_now_from_json,'%Y-%m-%dT%H:%M:%S.%fZ')).strftime("%H:%M:%S")
    except:
        date_now = '-'
        time = '-'
    print('yes 3')
    air_quality = Air_quality(id=str(id),
                              date=str(date_now),
                              pm25=str(resp['current']['values'][1].get('value')),
                              pm10=str(resp['current']['values'][2].get('value')),
                              temp=str(resp['current']['values'][5].get('value')),
                              aqi =str(aqi_value(resp['current']['values'][1].get('value')))
                            )

    air_quality.save()
    print('yes 4')
    #serializer = Air_QualitySerialization(air_quality)
    #serializer.data
    '''
    current[count][0]= str(id)
    current[count][1]= date_now
    current[count][2]= time
    try:
        current[count][3]= resp['current']['values'][1].get('value')
        current[count][4]= resp['current']['values'][2].get('value')
        current[count][5]= resp['current']['values'][5].get('value')
        current[count][6]= aqi_value(resp['current']['values'][1].get('value'))
    except:
        current[count][3]= 0
        current[count][4]= 0
        current[count][5]= 0
        current[count][6]= 0
    '''
    
def get_past(resp, start, id):
    global yesterday
    start = start
    count_hour = 0
    for hour in resp['history']:
        
        try:
            date_yesterday_from_json = hour.get("tillDateTime")
            date_yesterday = utc_to_local(datetime.strptime(date_yesterday_from_json,'%Y-%m-%dT%H:%M:%S.%fZ')).strftime("%d-%m-%Y")
            time = utc_to_local(datetime.strptime(date_yesterday_from_json,'%Y-%m-%dT%H:%M:%S.%fZ')).strftime("%H:%M:%S")
        except:
            date_yesterday = '-'
            time = '-'
        
        yesterday[start][0]= str(id)
        yesterday[start][1]= date_yesterday
        yesterday[start][2]= time
        
        try:
            yesterday[start][3] = hour['values'][1].get('value')
            yesterday[start][4] = hour['values'][2].get('value')
            yesterday[start][5] = hour['values'][5].get('value')
            yesterday[start][6] = aqi_value(hour['values'][1].get('value')) 
        except:
            yesterday[start][3] = 0
            yesterday[start][4] = 0
            yesterday[start][5] = 0
            yesterday[start][6] = 0
        
        start+=1
        count_hour+=1
    
    
def get_future(resp,start,id):
    global tomorrow
    start = start
    count_hour = 0
    for hour in resp['forecast']:
        try:
            date_tomorrow_from_json = hour.get("tillDateTime")
            date_tomorrow = utc_to_local(datetime.strptime(date_tomorrow_from_json,'%Y-%m-%dT%H:%M:%S.%fZ')).strftime("%d-%m-%Y")
            time = utc_to_local(datetime.strptime(date_tomorrow_from_json,'%Y-%m-%dT%H:%M:%S.%fZ')).strftime("%H:%M:%S")
        except:
            date_tomorrow = '-'
            time = '-'
        tomorrow[start][0] = str(id)
        tomorrow[start][1] = date_tomorrow
        tomorrow[start][2] = time
        try:
            tomorrow[start][3] = hour['values'][0].get('value')
            tomorrow[start][4] = hour['values'][1].get('value')
            tomorrow[start][5] = aqi_value(hour['values'][0].get('value'))
        except:
            tomorrow[start][3] = 0
            tomorrow[start][4] = 0
            tomorrow[start][5] = 0
        start+=1
    
def aqi_value(pm25):
    aqi = 0
    if 0<=pm25 and 12>=pm25 :
        aqi = ((50-0)/(12-0))*(pm25-0)+0
    elif 12<pm25 and 35.5>pm25 :
        aqi = ((100-51)/(35.4-12.1))*(pm25-12.1)+51
    elif 35.5<=pm25 and 55.5>pm25 :
        aqi = ((150-101)/(55.4-35.5))*(pm25-35.5)+101
    elif 55.5<=pm25 and 150.5>pm25 :
        aqi = ((200-151)/(150.4-55.5))*(pm25-55.5)+151
    elif 150.5<=pm25 and 250.5>pm25 :
        aqi = ((300-201)/(250.4-150.5))*(pm25-150.5)+201
    elif 250.5<=pm25 and 350.5>pm25 :
        aqi = ((400-301)/(350.4-250.5))*(pm25-250.5)+301
    elif 350.5<=pm25 and 500.4>=pm25 :
        aqi = ((500-401)/(500.4-350.5))*(pm25-350.5)+401
    return round(aqi)

