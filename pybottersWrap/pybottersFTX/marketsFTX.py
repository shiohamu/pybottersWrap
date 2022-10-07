import pybotters

class marketsFTX:

    def __init__(self,ticker,asset,pair,client:pybotters.Client):
        self.client = client
        self.ticker = ticker
        self.asset = asset
        self.pair = pair

    ################## Markets ################## 


    async def get_markets(self,market=None):
        """get markets"""
        url = "/markets"
        if market != None: url = "/markets/{}".format(market)
        r = await self.client.get(
            url
        )
        data = await r.json()
        return data["result"]

    async def get_market_orderbook(self, market=None, depth=20):
        """get market orderbook"""
        if market == None: market = self.pair
        r = await self.client.get(
            "/markets/{}/orderbook".format(market),
            params={"depth": depth}
        )
        data = await r.json()
        return data["result"]

    async def get_market_trades(self,market=None,page:dict=None) -> list:
        """get market trades"""
        if market == None: market=self.pair
        params = page
        r = await self.client.get(
            "/markets/{}/trades".format(market),
            params=params
        )
        data = await r.json()
        return data["result"]

    async def get_market_historical_prices(self,page:dict,market=None,resolution=300):
        """
        get market histrical prices\n
        Historical prices of expired futures can be retrieved with this end point but make sure to specify start time and end time.
        """
        if market == None: market = self.pair
        params = page
        params = params.setdefault("resolution", resolution)
        r = await self.client.get(
            "/markets/{}/candles".format(market),
            params=params
        )
        data = await r.json()
        return data["result"]


