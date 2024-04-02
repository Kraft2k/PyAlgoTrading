import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../QuikPy"))

sys.path.insert(1, os.path.join(sys.path[0], "../.."))
sys.path.insert(1, os.path.join(sys.path[0], ".."))


from QuikPy import QuikPy  # Working with QUIK from Python via QuikSharp LUA scripts
from backtrader_moexalgo.moexalgo_store import MoexAlgoStore  # Storage AlgoPack



class GetMoexInfo:

    def __init__(self, ticker_prefix):
        self.quik_provider = QuikPy()
        #self.store = MoexAlgoStore()
        self.ticker_prefix = ticker_prefix
        self.class_code = ticker_prefix

    def info_tickers(self, tickers):
        """ Getting information for the tickers """
        info = {}
        for _ticker in tickers:
            i = self.store.get_symbol_info(_ticker)
            info[f"{self.ticker_prefix}{_ticker}"] = i
        return info
    
    #['param_value']['data']

    def get_index(self, seccode):
        
        #print(self.quik_provider.GetParamEx(self.class_code, seccode, param_name ))
        
        keys= self.quik_provider.GetParamEx(self.class_code, seccode).keys()
        print(keys)
    def close_connection(self):
        self.quik_provider.CloseConnectionAndThread()



#TQOD.XS0088543193
#TQTF.LQDT

moex = GetMoexInfo('TQBR')
moex.get_index('SBER')

#print(moex.info_tickers(['XS0088543193', ]))

moex.close_connection()