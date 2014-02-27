#coding=utf8
import os, glob, ConfigParser, pybcs,re
from eden import bcsh, file_md5


class SyncStatic():
    def __init__(self, URL, AK, SK, BUCKET,EXCEPT):
        bcs = pybcs.BCS(URL, AK, SK, pybcs.HttplibHTTPC)
        self.bucket = bcs.bucket(BUCKET)
        self.excepts = EXCEPT

    def fun(self,path):
        for root,dirs,files in os.walk(path):
            for fn in files:
                if fn in self.excepts:
                    continue
                new = root.replace(path,'').replace("\\","/")
                objName = '/static' + new + '/' + fn
                fileName = root+"/"+fn
                fileName = fileName.replace("\\","/")
                o = self.bucket.object(objName)
                try:
                    #获取服务器上该文件的MD5
                    headInfo = o.head()
                    if headInfo:
                        md5 = headInfo['header']['content-md5']
                        md5info = file_md5.GetFileMd5(fileName)
                        if md5info[0] and md5info[1]==md5:
                            print '[skip]:There is no difference between two files!',objName
                            continue
                    print '[update]:',objName
                    o.put_file(fileName)
                except:
                    print '[add]:',objName
                    o.put_file(fileName,{"renametype":"md5"})

    def sync(self, path):
        self.fun(path)

if "__main__" == __name__:
    config = ConfigParser.ConfigParser()
    config.read("conf.ini")
    URL = config.get('bucket', 'URL')
    AK = config.get('bucket', 'AK')
    SK = config.get('bucket', 'SK')
    BUCKET = config.get('bucket', 'BUCKET')
    syncStatic = SyncStatic(URL, AK, SK, BUCKET,config.get('bucket','EXCEPT'))
    syncStatic.sync(os.getcwd())