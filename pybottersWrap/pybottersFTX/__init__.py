from platform import platform
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import pybotters
import asyncio
from configparser import ConfigParser

from .accountFTX import accountFTX
from .fillsFTX import fillsFTX
from .futuresFTX import futuresFTX
from .marketsFTX import marketsFTX
from .ordersFTX import ordersFTX
from .subaccountFTX import subaccountFTX
from .walletFTX import walletFTX
from .websocketFTX import websocketFTX

class pybottersFTX:
    def __init__(self,sub_account,ticker,asset):
        # only windows
        if("Windows" in platform()):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        # load api key
        key = ConfigParser()
        key.read("ini_file/key.ini")
        self.apis = {
            "ftx" : [key["ftx"]["api_key"],
                    key["ftx"]["api_secret"]]
        }

        # load url
        self.url = ConfigParser()
        self.url.read("ini_file/path.ini")
        self.ws_url = self.url["url"]["ftx_ws"]
        self.rest_url = self.url["url"]["ftx_rest"]

        # load config
        self.ticker = ticker
        self.asset = asset

        if((self.asset == "JPY") or (self.asset == "USD")):
            self.pair = self.ticker + "/" +  self.asset
        else:
            self.pair = self.ticker + "-" +  self.asset
        self.sub_account = sub_account
    
    async def __aenter__(self):
        header = None
        if(self.sub_account == ""):
            pass
        else:
            header = {"FTX-SUBACCOUNT": self.sub_account}
        self.client = pybotters.Client(apis=self.apis, base_url=self.rest_url, headers=header)

        # class init
        self.subaccount = subaccountFTX(self.ticker,self.asset,self.pair,self.client)
        self.markets = marketsFTX(self.ticker,self.asset,self.pair,self.client)
        self.futures = futuresFTX(self.ticker,self.asset,self.pair,self.client)
        self.account = accountFTX(self.ticker,self.asset,self.pair,self.client)
        self.wallet = walletFTX(self.ticker,self.asset,self.pair,self.client)
        self.orders = ordersFTX(self.ticker,self.asset,self.pair,self.client)
        self.fills = fillsFTX(self.ticker,self.asset,self.pair,self.client)
        self.websocket = websocketFTX(self.ticker,self.asset,self.pair,self.client,self.ws_url)

        return self.client

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.close()

    @property
    def get_timestamp(self):
        """get timestamp"""
        return int(time.time())

    def set_pagination(self,start_time,end_time):
        """set pagination"""
        params={}
        params.setdefault("start_time", start_time)
        params.setdefault("end_time", end_time)
        return params

    def set_pagination(self,date:list,minute_span):
        """set pagination"""
        params={}
        start_time = datetime(*date)
        end_time = start_time
        end_time = end_time + relativedelta(minute=minute_span)
        params.setdefault("start_time", start_time.timestamp())
        params.setdefault("end_time", end_time.timestamp())
        return params
    
    # set parameters
    def set_parameters(self, params:dict=None, **kargs):
        if(params == None):
            params = {}
        now_params = params
        for key, value in kargs.items():
            now_params.setdefault(key, value)
        return now_params


    # test method
    async def test(self,ftx:pybotters.Client):
            async with ftx as client:
                data = self.websocket.set_datastores_endpoint()
                subscribe = self.websocket.set_subscribe(["orderbook","fills"])
                wstask, store = await self.websocket.ws_init(client,data,subscribe)
                
                market = await self.markets.get_markets()
                for m in market:
                    print("{} ".format(m["name"]))

if __name__ == "__main__":
    ftx = pybottersFTX("BTC","PERP")
    asyncio.run(ftx.test(ftx))