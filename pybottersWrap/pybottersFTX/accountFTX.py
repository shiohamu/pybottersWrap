import pybotters
import time

class accountFTX:

    def __init__(self,ticker,asset,pair,client:pybotters.Client):
        self.client = client
        self.ticker = ticker
        self.asset = asset
        self.pair = pair

    @property
    def get_timestamp(self):
        """get timestamp"""
        return int(time.time())

    ################## Account ################## 


    @property
    async def get_account_info(self):
        """get account information"""
        r = await self.client.get(
            "/account"
        )
        data = await r.json()
        return data["result"]

    async def request_historical_snapshot(self,accounts:list,end_time=None):
        """request historical balance and positions snapshot"""
        if end_time == None: end_time = self.get_timestamp
        params = {"accounts": accounts, "endTime": end_time}
        r = await self.client.post(
            "/historical_balances/requests",
            data=params
        )
        data = await r.json()
        return data["result"]

    async def get_historical_snapshot(self,accounts:list,end_time=None):
        """get histrical balances and positions snapshot"""
        id = await self.request_historical_snapshot(accounts,end_time)
        r = await self.client.get(
            "/historical_balances/requests/{}".format(id)
        )
        data = await r.json()
        return data["result"]
        
    async def get_all_historical_snapshots(self):
        """get all historical balances and position snapshots"""
        r = await self.client.get(
            "/historical_balances/requests"
        )
        data = await r.json()
        return data["result"]
    
    async def get_positions(self,showAvgPrice=False):
        """get positions"""
        params = None
        if showAvgPrice: params = {"showAvgPrice": "true"}
        else: params = {"showAvgPrice": "false"}
        r = await self.client.get(
            "/positions",
            params=params
        )
        data = await r.json()
        return data["result"]

    async def change_leverage(self,leverage):
        """change account leverage"""
        r = await self.client.post(
            "/account/leverage",
            data={"leverage": leverage}
        )
        data = await r.json()
        return data["result"]
