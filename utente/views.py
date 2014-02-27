#coding=utf8
from django.shortcuts import render
from utente.models import *
import urllib,urllib2,json,base64,re
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.utils.http import urlunquote
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template import RequestContext

def to_login(request):
    next = request.GET.get('next')
    return render_to_response('utente/login.html',{'next':next},context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return render_to_response('utente/login.html',context_instance=RequestContext(request))

def valid_login(request):
    userName = request.POST.get('userName')
    userPwd = request.POST.get('userPwd')
    next = request.POST.get('next')
    user = auth.authenticate(username=userName,password=userPwd)
    if user is not None and user.is_active:
        auth.login(request,user)
        if next is None or next=="":
            next ="/"
        return HttpResponseRedirect(next)
    return render_to_response('utente/login.html',{'error':True,'message':'用户名或密码错误'},context_instance=RequestContext(request))

def getWeatherByCityName(request,cityName):
    city = cityName
    if re.search(r"(%\w{2})", cityName):
        city = urlunquote(cityName)
    response = HttpResponse()
    try:
        cityInfo = CityInfo.objects.get(areaName=city)
        url = 'http://www.weather.com.cn/data/cityinfo/%s.html' %cityInfo.cityCode
        req = urllib2.Request(url)
        req.add_header('User-Agent', "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)")
        fp = urllib2.urlopen(req)
        result = fp.read()
        base64str = base64.encodestring(result)
        #将获取到的天气情况放入cookie中，过期时间：30分钟
        response.set_cookie('remote_city_weather',base64str,expires=1800)
        response.write(result)
    except:
        response.write('')
    return response