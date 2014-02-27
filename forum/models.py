#coding=utf8
from django.db import models
from django.contrib.auth.models import User

class BlogType(models.Model):
    type_key = models.CharField(max_length=50,verbose_name='分类编码')
    type_name = models.CharField(max_length=50,verbose_name='分类名称')
    def __unicode__(self):
        return self.type_name
    class Meta:
        ordering = ['type_key']

class Blog(models.Model):
    type_id = models.ForeignKey(BlogType,verbose_name='博客类型')
    author = models.ForeignKey(User,verbose_name='作者')
    subject = models.CharField(max_length=200,verbose_name='标题')
    content = models.TextField(verbose_name='文本内容')
    html = models.TextField(verbose_name='html内容')
    tag = models.CharField(max_length=200,verbose_name='标签')
    picture = models.FilePathField(verbose_name='图片',blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间',auto_now_add=True)
    publish = models.SmallIntegerField(verbose_name='已发布')
    view_time = models.SmallIntegerField(verbose_name='浏览次数')
    def __unicode__(self):
        return self.subject
    class Meta:
        ordering = ['-create_time']

class BlogComment(models.Model):
    author = models.ForeignKey(User,verbose_name='作者')
    blog_id = models.ForeignKey(Blog,verbose_name='评论博客')
    reply_id = models.CharField(max_length=50,verbose_name='回复评论')
    content = models.TextField(verbose_name='评论内容')
    create_time = models.DateTimeField(verbose_name='评论时间',auto_now_add=True)
    top = models.SmallIntegerField(verbose_name='被顶次数')
    percor = models.SmallIntegerField(verbose_name='被踩的次数')
    def __unicode__(self):
        return self.content
    class Meta:
        ordering = ['-create_time']
