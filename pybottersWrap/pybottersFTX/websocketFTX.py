import pybotters

class websocketFTX:

    def __init__(self,ticker,asset,pair,client:pybotters.Client,ws_url):
        self.client = client
        self.ticker = ticker
        self.asset = asset
        self.pair = pair
        self.ws_url = ws_url

        # init datastore
        self.store = pybotters.FTXDataStore()

    ################## WebSocket ################## 


    async def ws_init(self,client:pybotters.Client,data,subscribe):
        """WebSocket initialize"""
        await self.store.initialize(
            *data
        )
        wstask = await client.ws_connect(
            self.ws_url,
            send_json=[*subscribe],
            hdlr_json=self.store.onmessage
        )

        return wstask, self.store

    def set_datastores_endpoint(self,orders=True,conditional_orders=False,positions=True):
        """set datastores endpoint"""
        data = []
        if orders: 
            data.append(self.client.get("/orders", params={"market": self.pair}))
        elif conditional_orders: 
            data.append(self.client.get("/conditional_orders", params={"market": self.pair}))
        if positions: 
            data.append(self.client.get("/positions", params={"showAvgPrice": "true", "market": self.pair}))
        
        return data
    
    def set_subscribe(self,channels:list=["orderbook"],markets:list=None,op="subscribe"):
        """set subscribe"""
        subscribe = []
        if markets == None: markets = [self.pair]
        for channel in channels:
            for market in markets:
                subscribe.append({"op": op, "channel": channel, "market": market})
        
        return subscribe

