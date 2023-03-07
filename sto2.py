import sto3
from collections import namedtuple

KEY = sto3.key_data
KEY = KEY.split(',')

class B:
    def __init__(self):
        self.REALTYPE = dict()
        self.REALTYPE['int'] = dict()
        
        for k in KEY:
            self.REALTYPE['int'][k] = 1
        

class A:
    def dynamicCall(self, s, c, k):
        return s, c, k   
    
    def get_data(self, sCode, sRealType, string):
        r = self.dynamicCall("GetCommRealData(QString, int)", sCode,self.realType.REALTYPE[sRealType][string])
        try:
            return float(r)
        except:
            return r
    
    def __init__(self,sCode, sRealType):
        self.realType = B()
        data = namedtuple("Data", [f'v{i}' for i in range(len(KEY))])
        xx = []
        for k in KEY:
            xx.append(self.get_data(sCode, sRealType, k))
        k = data(*xx)
        print(k)

        # import pprint
        # pprint.pprint(data)
        

a = A("code", "int")