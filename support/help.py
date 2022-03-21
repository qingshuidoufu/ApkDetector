import io
from hashlib import md5


class myErr(Exception):
    def __init__(self,msg):
        self.msg=msg;
    def __str__(self):
        return repr(self.msg)

def calMD5(filePath):
    file=io.FileIO(filePath,'r')
    m=md5()
    bytes=file.read(1024)
    while(bytes!=b''):
        m.update(bytes)
        bytes=file.read(1024)
    file.close()
    return m.hexdigest()

