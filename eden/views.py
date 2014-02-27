#coding=utf8
from django.shortcuts import render_to_response
from django.http import HttpResponse
import time,uuid
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext

def main_page(request):
    signature = request.GET.get('signature')
    echostr = request.GET.get('echostr')
    if signature and echostr:
        return HttpResponse(echostr)
    #authorizationCode = request.GET.get('code')
    #accessToken = request.GET.get('access_token')
    #if authorizationCode:
    #    values = {'grant_type': 'authorization_code', 'client_id': '100589044',
    #              'client_secret': "f00b902fad76a72acf24c9d4cc2ef3cf", 'code': authorizationCode,
    #              'redirect_uri':'52dudu.duapp.com'}
    #    d = urllib.urlencode(values)
    #    url = 'https://graph.qq.com/oauth2.0/token?%s' %d
    #    req = urllib2.Request(url)
    #    req.add_header('User-Agent', "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)")
    #    fp = urllib2.urlopen(req)
    #    result = fp.read()
    c = RequestContext(request)
    return render_to_response('index.html', {'curModule': 'main'},context_instance=RequestContext(request))

def just_say(request):
    return render_to_response('fun/say.html', {'curModule': 'say'},context_instance=RequestContext(request))

def about_me(request):
    return render_to_response('fun/about.html', {'curModule': 'about'},context_instance=RequestContext(request))

def photo_wall(request):
    return render_to_response('photo/photoWall.html', {'curModule': 'photo'},context_instance=RequestContext(request))

@login_required
def message(request):
    fullname = request.user.get_full_name()
    return render_to_response('fun/message.html', {'curModule': 'message'},context_instance=RequestContext(request))


@csrf_exempt
def upload_file(request):
    type = request.GET.get("type")
    editorid = request.GET.get("editorid")
    url = ''
    if request.method == 'POST':
        try:
            url = save_file(request.FILES['upfile'])
        except Exception as e:
            print e
    if type == 'ajax':
        return HttpResponse(url)
    b = "<script>parent.UM.getEditor('%s').getWidgetCallback('image')('%s','SUCCESS')</script>" %(editorid,url)
    return HttpResponse(b)

def save_file(file):
    filename = file.name.decode('utf-8', 'ignore')
    fileExt = filename.split('.')[1]
    newname = str(uuid.uuid1()) + '.' + fileExt
    newname = newname.encode()
    #bcs = pybcs.BCS('http://bcs.duapp.com/', 'LG8ho1Q3StSgnH2Orj9ES4sB', 'OScgWpOQO2CYUiLncmG3pwRQEe7Lg3SS', pybcs.HttplibHTTPC)
    #bucket = bcs.bucket('dudufile')
    monthStr = time.strftime('%Y%m',time.localtime(time.time()))
    path = '/forum/%s/%s' %(monthStr,newname)
    a = 'http://bcs.duapp.com/dudufile%s' %path
    return a