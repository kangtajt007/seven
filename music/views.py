#coding=utf8
from django.shortcuts import render_to_response
from django.http import HttpResponse
import urllib,urllib2,json,re
from django.template import RequestContext

#音乐盒
def music_box(request):
    return render_to_response('fun/music.html',{'curModule':'music'},context_instance=RequestContext(request))

def query_musiz(request,word):
    word = word.encode('utf8')
    values = {'tn':'getinfo','ct':'0','ie':"utf-8",'format':'json'}
    d = urllib.urlencode(values)
    url = 'http://mp3.baidu.com/dev/api/?%s' %d
    url = url + '&word=%s' %word
    req = urllib2.Request(url)
    req.add_header('User-Agent', "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)")
    fp = urllib2.urlopen(req)
    result = fp.read()
    response = HttpResponse()
    response['Content-Type'] = fp.headers.dict["content-type"]
    #重试次数
    maxRetry = 7
    while maxRetry > 0 and result.strip()=='[]':
        maxRetry = maxRetry-1
        fp = urllib2.urlopen(req)
        result = fp.read()
    fp.close()

    response.write(result)
    return response

def get_song(request,id):
    values = {'songIds':id}
    d = urllib.urlencode(values)
    url = 'http://ting.baidu.com/data/music/links?%s' %d
    req = urllib2.Request(url)
    req.add_header('User-Agent', "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)")
    fp = urllib2.urlopen(req)
    result = fp.read()
    fp.close()
    data = json.loads(result)
    data = json.dumps(data)
    response = HttpResponse()
    response.write(data)
    return response

def get_song_data(request,address):
    songUrl = request.get_full_path()
    songUrl = re.sub("&63;", "?", songUrl)
    songUrl = re.sub("&58;", ":", songUrl)
    songUrl = re.sub("&47;", "/", songUrl)
    songUrl = re.sub("%22", "\"", songUrl)
    songUrl = songUrl.split("path=")
    songUrl = songUrl[1]
    req = urllib2.Request(songUrl)
    req.add_header('User-Agent', "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)")
    fp = urllib2.urlopen(req)
    response = HttpResponse()
    response['Content-Type'] = "audio/mpeg"
    response['Content-Length'] = fp.headers.dict["content-length"]
    while 1:
        s = fp.read(8192)
        if not s:
            break
        response.write(s)
    fp.close()
    return response

def get_lrc(request,address):
    url = 'http://ting.baidu.com/%s' %address
    req = urllib2.Request(url)
    req.add_header('User-Agent', "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)")
    fp = urllib2.urlopen(req)
    lrc = ''
    response = HttpResponse()
    while 1:
        s = fp.read(8192)
        if not s:
            break
        lrc += s
    fp.close()
    response.write(lrc)
    return response