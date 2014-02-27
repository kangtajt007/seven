from django.shortcuts import render_to_response
from forum.models import *
from django.template import RequestContext
from forms import *
from django.contrib.auth.decorators import login_required

def blog_list(request,index = 1):
    blogs = Blog.objects.filter(publish=1)
    size = blogs.count()
    return render_to_response('forum/BlogList.html',{'curModule':'blog','blogs':blogs,'page':{'index':index,'count': size}},context_instance=RequestContext(request))

def blog_get(request,id):
    blog = Blog.objects.get(id=id)
    blog.view_time = blog.view_time + 1
    blog.save()
    return render_to_response('forum/BlogDetail.html',{'curModule':'blog','blog':blog},context_instance=RequestContext(request))

def blog_list_by_type(request,type_id,index=1):
    blog_type = BlogType.objects.get(id=type_id)
    blogs = Blog.objects.filter(type_id=type_id).filter(publish=1)
    size = blogs.count()
    return render_to_response('forum/BlogList.html',{'curModule':'blog','blog_type':blog_type,'blogs':blogs,'page':{'index':index,'count': size}},context_instance=RequestContext(request))

@login_required
def blog_edit(request):
    types = BlogType.objects.all()
    c = RequestContext(request)
    return render_to_response('forum/BlogEdit.html',{'curModule':'blog','types':types},context_instance=RequestContext(request))

@login_required
def save_blog(request):
    return render_to_response()

@login_required
def deploy_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blogForm = form.cleaned_data
            blogType = BlogType.objects.get(id=blogForm["type"])
            blog = Blog()
            blog.author = request.user
            blog.type_id = blogType
            blog.subject = blogForm["subject"]
            blog.content = blogForm["content"]
            blog.html = blogForm["myEditor"]
            blog.tag = blogForm["tag"]
            blog.picture = "1"
            blog.publish = 1
            blog.view_time = 0
            blog.save()
        return render_to_response('result.html',{})
    else:
        form = BlogForm()
    return render_to_response('contact_form.html', {'form': form},context_instance=RequestContext(request))