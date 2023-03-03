KEY = '체결시간,체결강도,현재가,전일대비,등락율,(최우선)매도호가,(최우선)매수호가,거래량,누적거래량,누적거래대금,고가,시가,저가,시가총액(억),전일거래량대비(비율),거래회전율,전일동시간거래량비율'        

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