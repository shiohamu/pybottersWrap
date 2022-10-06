import pybotters

class fillsFTX:

    def __init__(self,ticker,asset,pair,client:pybotters.Client):
        self.client = client
        self.ticker = ticker
        self.asset = asset
        self.pair = pair

    ################## Fills ################## 


    async def fills(self,
        market=None,
        order=None,
        orderId=None,
        page=None):
        """Fills"""
        params = {}
        if page != None: params = page
        if market != None: params.setdefault("market", market)
        if order != None: params.setdefault("order", order)
        if orderId != None: params.setdefault("orderId", orderId)

        r = await self.client.get(
            "/fills",
            params=params
        )
        data = await r.json()
        return data["result"]