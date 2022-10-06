import pybotters

class futuresFTX:
    
    def __init__(self,ticker,asset,pair,client:pybotters.Client):
        self.client = client
        self.ticker = ticker
        self.asset = asset
        self.pair = pair

    ################## Futures ################## 


    async def get_futures(self,market=None):
        """get futures data"""
        url = "/futures"
        if market != None: url = "/futures/{}".format(market)
        r = await self.client.get(
            url
        )
        data = await r.json()
        return data["result"]

    async def get_futures_stats(self,market=None):
        """get futures stats"""
        if market == None: market = self.pair
        r = await self.client.get(
            "/futures/{}/stats".format(market)
        )
        data = await r.json()
        return data["result"]

    async def get_funding_rates(self,page:dict=None,future=None):
        """get funding rates"""
        if future == None: future = self.pair
        if page == None: page = {}
        params = page
        params.setdefault("future", future)
        r = await self.client.get(
            "/funding_rates",
            params=params
        )
        data = await r.json()
        return data["result"]

    async def get_futures_incex_weights(self,index="ALT"):
        """
        get futures index weights\n
        Note that this only applies to index futures, e.g. ALT/MID/SHIT/EXCH/DRAGON.
        """
        r = await self.client.get(
            "/indexes/{}/weights".format(index)
        )
        data = await r.json()
        return data["result"]

    @property
    async def get_expired_futures(self):
        """get expires futures\n
        Returns the list of all expired futures.
        """
        r = await self.client.get(
            "/expired_futures"
        )
        data = await r.json()
        return data["result"]

    async def get_futures_historical_index(self,ticker=None,resolution=300,page:dict=None):
        """get futures historical index"""
        if ticker == None: ticker = self.ticker
        if page == None: page = {}
        params = page
        params.setdefault("resolution", resolution)
        r = await self.client.get(
            "/indexes/{}/candles".format(ticker),
            params=params
        )
        data = await r.json()
        return data["result"]

    async def get_futures_index_constituents(self,ticker=None):
        """get index consituents"""
        if ticker == None: ticker = self.ticker
        r = await self.client.get(
            "/index_constituents/{}".format(ticker)
        )
        data = await r.json()
        return data["result"]
