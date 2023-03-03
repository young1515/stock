import pymysql
from datetime import timedelta
from collections import defaultdict
# #sql2 = "select code,time,open,low,high,close,t_amount,date from make_ticks where code in('000020','000040','000050','000060','000070','000080','000100','000120','000140','000150')  and date =20221208  and  time > 090000 order by time asc limit 5"
# sql2 = "select code,time,open,low,high,close,t_amount,date from make_ticks where code in('000060')  and date =20221208  and  time > 090000 order by time asc limit 5000"

SQL_LOAD = "select code,time,open,low,high,close,t_amount,date from make_ticks where code in('000060','000050','000020','000080','000120')  and date =20221208  and  time > 090000 order by time asc LIMIT 1200"
ID = 'baritstock'
PASS = 'Dlckddudcjswo2@@'


class Tick:
    def __init__(self, data):
        self.name = data['name']
        self.code = data['code']
        self.date = data['time']
        self.close = data['close']
        self.volume = data['volume']
        self.buy_volume = data['buy_volume']


class Data:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self._date = None
        self._open = None
        self._high = None
        self._low = None
        self._close = None
        self._volume = 0
        self._buy_volume = 0
        self._x_ray = None
        self._v_amount = None
        self._min_1 = []
        self._min_5 = []
        self._min_15 = []
        self._min_30 = []
        self._tick_15 = []
    @property
    def close(self):
        return self._close
    @close.setter
    def close(self, data):
        self._close = data
        if self.high <= data:
            self.high = data
        if self.low >= data:
            self.low = data
    @property
    def low(self):
        return self._low
    @low.setter
    def low(self, data):
        self._low = data
    @property
    def high(self):
        return self._high
    @high.setter
    def high(self, data):
        self._high = data


        
class BunBong:
    def __init__(self, start_time, end_time, base, code, start):
        self.start_time = start_time
        self.end_time = end_time
        self.base = base
        self.code = code
        self.start = start
        self.high = start
        self.low = start
        self.close = start
    def set_high(self, high):
        if high > self.high:
            self.high = high
    def set_low(self, low):
        if low < self.low:
            self.low = low
    def set_close(self, close):
        self.close = close
    def set_end_time(self, end_time):
        self.end_time = end_time
    def __str__(self):
        return str((self.base, 'code:', self.code, '시:',self.start, '고:',self.high, '저:', self.low, '종:', self.close))
    def __repr__(self):
        return str((self.start_time, self.end_time, self.base, 'code:', self.code, '시:',self.start, '고:',self.high, '저:', self.low, '종:', self.close))


class Maindict():
    def __init__(self):
        self.conn = pymysql.connect(host='vellusha.synology.me', user=ID,
                                    password=PASS, port=13306, db='stock', charset='utf8',
                                    autocommit=True,
                                    cursorclass=pymysql.cursors.DictCursor  # 결과 DB 반영 (Insert or update)
                                    )
        self.curs = self.conn.cursor()
        self.calcul_dict = {}
        self.be_min_candle =  None

        self.make_dic_set()
        self.make_mins(1)

        # 분봉 시간 간격
        self.minute_interval = 1

    def make_dic_set(self):
        sql = "select * from company_all_info2 limit 10"
        self.curs.execute(sql)
        # print(curs.fetchall())
        row_company = self.curs.fetchall()
        for i in range(len(row_company)):
            # print(row_company[i]['code'])
            self.calcul_dict[row_company[i]['code']] = {}
            self.calcul_dict[row_company[i]['code']].update({'name':row_company[i]['company'] })
            self.calcul_dict[row_company[i]['code']].update({'date': 0})
            self.calcul_dict[row_company[i]['code']].update({'open':0})
            self.calcul_dict[row_company[i]['code']].update({'high': 0})
            self.calcul_dict[row_company[i]['code']].update({'low': 0})
            self.calcul_dict[row_company[i]['code']].update({'close': 0})
            self.calcul_dict[row_company[i]['code']].update({'volume': 0})
            self.calcul_dict[row_company[i]['code']].update({'buy_volume': 0})
            self.calcul_dict[row_company[i]['code']].update({'x_ray': 0})
            self.calcul_dict[row_company[i]['code']].update({'v_amount': 0})
            self.calcul_dict[row_company[i]['code']].update({'1mins': []})
            '''
            self.calcul_dict[row_company[i]['code']].update({'5mins': []})
            self.calcul_dict[row_company[i]['code']].update({'15mins': []})
            self.calcul_dict[row_company[i]['code']].update({'30mins': []})
            self.calcul_dict[row_company[i]['code']].update({'tick150': []})
            '''

    def make_mins(self, unit_time):
        self.curs.execute(SQL_LOAD)
        row_tick_data = self.curs.fetchall()
        started_time = dict()
        bunbong = dict()
        min_data = defaultdict(int)
        bunbongs = defaultdict(list)
        
        
        for idx in range(len(row_tick_data)):
            
            code = row_tick_data[idx]['code']
            tick_data:dict = row_tick_data[idx]
            open_data = tick_data['open']
            time_data = tick_data['time']
            low_data = tick_data['low']
            high_data = tick_data['high']
            close_data = tick_data['close']
            min_data_code = min_data[code]
            if code not in started_time:
                started_time[code] = time_data
            if code not in bunbong:
                bunbong[code] = BunBong(time_data, time_data, 0, code, open_data)
            bunbongs_code:list = bunbongs[code]
            if timedelta(minutes=min_data_code) <= (time_data-started_time[code]):
                bunbongs_code.append(bunbong[code])
                bunbong[code] = BunBong(time_data, time_data, min_data_code, code, open_data)
                min_data[code] += unit_time
            bunbong_code:BunBong = bunbong[code]
            bunbong_code.set_low(low_data)
            bunbong_code.set_high(high_data)
            bunbong_code.set_close(close_data)
            bunbong_code.set_end_time(time_data)

        import pprint
        pprint.pprint(bunbongs)
if __name__ == "__main__":
    Maindict()