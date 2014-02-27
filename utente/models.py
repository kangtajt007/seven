#coding=utf8
from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=30,verbose_name='名称')
    account = models.CharField(max_length=30,verbose_name='账号')
    website = models.URLField(verbose_name='网址')
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

class CityInfo(models.Model):
    provinceId = models.CharField(max_length=30,verbose_name='所在省ID')
    provinceName = models.CharField(max_length=400,verbose_name='所在省名称')
    townId = models.CharField(max_length=30,verbose_name='所在城市ID')
    townName = models.CharField(max_length=400,verbose_name='所在城市名称')
    areaId = models.CharField(max_length=30,verbose_name='所在区ID')
    areaName = models.CharField(max_length=400,verbose_name='所在区名称')
    cityCode = models.CharField(max_length=100,verbose_name='城市代码')
    def __unicode__(self):
        return self.areaName
    class Meta:
        ordering = ['areaId']