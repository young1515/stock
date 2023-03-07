import sto3

KEY = sto3.key_data

class B:
    def __init__(self):
        self.REALTYPE = dict()
        self.REALTYPE['int'] = dict()
        
        for k in KEY.split(','):
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
        data = dict()
        for k in KEY.split(','):
            data[k] = self.get_data(sCode, sRealType, k)
        import pprint
        pprint.pprint(data)
        
        
a = A("code", "int")