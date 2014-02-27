import sys,hashlib

def GetFileMd5(strFile):  
    file = None
    bRet = False
    strMd5 = ""
      
    try:  
        file = open(strFile, "rb");  
        md5 = hashlib.md5()
        strRead = ""
          
        while True:  
            strRead = file.read(8096)
            if not strRead:  
                break
            md5.update(strRead)
        #read file finish  
        bRet = True
        strMd5 = md5.hexdigest()
    except:  
        bRet = False
    finally:  
        if file:  
            file.close()  
    return [bRet, strMd5]