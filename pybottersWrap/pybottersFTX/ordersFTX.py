import pybotters

class ordersFTX:

    def __init__(self,ticker,asset,pair,client:pybotters.Client):
        self.client = client
        self.ticker = ticker
        self.asset = asset
        self.pair = pair

    ################## Orders ################## 


    async def get_open_orders(self,market=None):
        """get open orders"""
        if market == None: market = self.pair
        r = await self.client.get(
            "/orders",
            params={"market": market}
        )
        data = await r.json()
        return data["result"]

    async def get_order_history(self,market=None,side=None,orderType=None,page=None):
        """get order history"""
        params = {}
        if page != None: params = page
        if market == None: params.setdefault("market", market)
        if side != None: params.setdefault("side", side)
        if orderType != None: params.setdefault("orderType", orderType)
        r = await self.client.get(
            "/orders/history",
            params=params
        )
        data = await r.json()
        return data["result"]

    async def get_open_trigger_orders(self,market,order_type=None):
        """get open trigger orders"""
        params = {"market": market}
        if order_type != None: params.setdefault("type", order_type)
        r = await self.client.get(
            "/conditional_orders",
            params=params
        )
        data = await r.json()
        return data["result"]

    async def get_trigger_order_triggers(self,conditinal_order_id):
        """get trigger order triggers"""
        r = await self.client.get(
            "/conditional_orders/{}/triggers".format(conditinal_order_id)
        )
        data = await r.json()
        return data["result"]

    async def get_trigger_order_history(self,market=None,page=None):
        """get trigger order history"""
        params = {}
        if page != None: params = page
        if market != None: params.setdefault("market", market)
        r = await self.client.get(
            "/conditional_orders/history",
            params=params
        )
        data = await r.json()
        return data["result"]

    async def get_twap_orders(self,market=None,page=None):
        """get TWAP orders"""
        params = {}
        if page != None: params = page
        if market != None: params.setdefault("market", market)
        
        r = await self.client.get(
            "/twap_orders",
            params=params
        )
        data = await r.json()
        return data["result"]

    async def get_twap_order_executions(self,twap_order_id,page):
        """get TWAP order execution"""
        params = {}
        if page != None: params = page
        r = await self.client.get(
            "/twap_orders/{}/executions".format(twap_order_id),
            params=params
        )
        data = await r.json()
        return data["result"]

    async def place_order(self,
        side,
        size,
        market=None,
        price=None,
        order_type="market",
        reduceOnly=False,
        ioc=False,
        postOnly=False,
        clientId=None,
        rejectOnPriceBand=False,
        rejectAfterTs=None):

        """place order"""
        if market == None: market = self.pair
        params = {
            "market": market,
            "side": side,
            "type": order_type,
            "size": size,
        }
        if order_type in "market": params.setdefault("price", None)
        elif order_type in "limit": params.setdefault("price", price)
        if reduceOnly: params.setdefault("reduceOnly", reduceOnly)
        if ioc: params.setdefault("ioc", ioc)
        if postOnly and order_type in "limit": params.setdefault("postOnly", postOnly)
        if clientId != None: params.setdefault("clientId", clientId)
        if rejectOnPriceBand: params.setdefault("rejectOnPriceBand", rejectOnPriceBand)
        if rejectAfterTs != None: params.setdefault("rejectAfterTs", rejectAfterTs)

        r = await self.client.post(
            "/orders",
            data=params
        )
        data = await r.json()
        if(data["success"]):
            return data["result"]
        else:
            return None

    async def place_trigger_order(self,
        side,
        size,
        market=None,
        order_type="stop",
        reduceOnly=False,
        retryUntilFilled=False,
        triggerPrice=None,
        orderPrice=None,
        trailValue=None
        ):
        """
        place trigger order\n
        Trigger orders include stop, trailing stop, and take profit.
        """

        if market == None: market = self.pair

        params = {
            "market": market,
            "side": side,
            "size": size,
            "type": order_type,
        }

        if not reduceOnly: params.setdefault("reduceOnly", reduceOnly)
        if not retryUntilFilled: params.setdefault("retryUntilFilled", retryUntilFilled)

        # order type detect
        if order_type in "trailingStop":
            params.setdefault("trailValue", trailValue)
            
        elif order_type in ("stop", "takeProfit"):
            params.setdefault("triggerPrice", triggerPrice)
            if orderPrice != None: params.setdefault("orderPrice", orderPrice)

        else: return None

        r = await self.client.post(
            "/conditional_orders",
            data=params
        )
        data = await r.json()
        return data["result"]

    async def place_twap_order(self,
        side,
        size,
        market=None,
        order_type="market",
        durationSeconds=600,
        randomizeSize=False,
        maxSpread=None,
        maxIndividualOrderSize=None,
        maxDistanceThroughBook=None,
        priceBound=None
        ):
        """place TWAP order"""
        if market == None: market = self.pair
        params = {
            "market": market,
            "side": side,
            "size": size,
            "type": order_type,
            "durationSecounds": durationSeconds,
        }

        if not randomizeSize: params.setdefault("randomizeSize", randomizeSize)
        if maxSpread != None: params.setdefault("maxSpread", maxSpread)
        if maxIndividualOrderSize != None: params.setdefault("maxIndividualOrderSize", maxIndividualOrderSize)
        if maxDistanceThroughBook != None: params.setdefault("maxDistanceThroughBook", maxDistanceThroughBook)
        if priceBound != None: params.setdefault("priceBound", priceBound)

        r = await self.client.post(
            "/twap_orders",
            data= params
        )
        data =  await r.json()
        return data["result"]
        
    async def modify_order(self,
        order_id,
        price=None,
        size=None,
        clientId=None):
        """
        Modify order\n
        Please note that the order's queue priority will be reset, and the order ID of the modified order will be different from that of the original order. Also note: this is implemented as cancelling and replacing your order. There's a chance that the order meant to be cancelled gets filled and its replacement still gets placed.
        """

        params = {}
        if price != None: params.setdefault("price", price)
        if size != None: params.setdefault("size", size)
        if clientId != None: params.setdefault("clientId", clientId)

        r = await self.client.post(
            "/orders/{}/modify".format(order_id),
            data=params
        )
        data = await r.json()
        
        if(data["success"]):
            return data["result"]
        else:
            return None

    
    async def modify_order_by_clientId(self,
        client_order_id,
        price=None,
        size=None,
        clientId=None):
        """
        Modify order by client ID\n
        Please note that the order's queue priority will be reset, and the order ID of the modified order will be different from that of the original order. Also note: this is implemented as cancelling and replacing your order. There's a chance that the order meant to be cancelled gets filled and its replacement still gets placed.
        """

        params = {}
        if price != None: params.setdefault("price", price)
        if size != None: params.setdefault("size", size)
        if clientId != None: params.setdefault("clientId", clientId)

        r = await self.client.post(
            "/orders/by_client_id/{}/modify".format(client_order_id),
            data=params
        )
        data = await r.json()
        return data["result"]

    async def modify_trigger_order(self,
        order_id,
        size,
        triggerPrice=None,
        orderPrice=None,
        trailValue=None):
        """Modify trigger order\n
        Trigger orders include stop, trailing stop, and take profit.\n
        Please note that the order ID of the modified order will be different from that of the original order.\n
        """

        params = {"size": size}

        # order_type detect
        if trailValue != None:
            params.setdefault("trailValue", trailValue)
        elif triggerPrice != None and orderPrice != None:
            params.setdefault("triggerPrice", triggerPrice)
            params.setdefault("orderPrice", orderPrice)
        else: return None

        r = await self.client.post(
            "/conditional_orders/{}/modify".format(order_id),
            data=params
        )
        data = await r.json()
        return data["result"]

    async def get_order_status(self,order_id):
        """get order status"""
        r = await self.client.get(
            "/orders/{}".format(order_id)
        )
        data = await r.json()
        return data["result"]
    
    async def get_order_status_by_clientId(self,client_order_id):
        """get order status by client ID"""
        r = await self.client.get(
            "/orders/by_client_id/{}".format(client_order_id)
        )
        data = await r.json()
        return data["result"]

    async def cancel_order(self,order_id):
        """cancel order"""
        r = await self.client.delete(
            "/orders/{}".format(order_id)
        )
        data = await r.json()
        return data["result"]

    async def cancel_twap_order(self,twap_order_id):
        """cancel TWAP order"""
        r = await self.client.delete(
            "/twap_orders/{}".format(twap_order_id)
        )
        data = await r.json()
        return data["result"]

    async def cancel_order_by_clientId(self,client_order_id):
        """cancel order by client ID"""
        r = await self.client.delete(
            "/orders/by_client_id/{}".format(client_order_id)
        )
        data = await r.json()
        return data["result"]

    async def cancel_all_orders(self,
        market=None,
        side=None,
        conditionalOrdersOnly=False,
        limitOrdersOnly=False):
        """
        Cancel all orders\n
        This will also cancel conditional orders (stop loss and trailing stop orders.
        """
        params = {}
        if market != None: params.setdefault("market", market)
        if side != None: params.setdefault("side", side)
        if not conditionalOrdersOnly: params.setdefault("conditionalOrdersOnly", conditionalOrdersOnly)
        if not limitOrdersOnly: params.setdefault("limitOrdersOnly", limitOrdersOnly)

        r = await self.client.delete(
            "/orders",
            data=params
        )
        data = await r.json()
        return data["result"]
    
    async def bulk_cancel_orders(self,orderIds:list):
        """Bulk cancel orders"""
        r = await self.client.delete(
            "/bulk_orders",
            data={"orderIds": orderIds}
        )
        data = await r.json()
        return data["result"]

    async def bulk_cancel_orders_by_clientId(self,clientOrderIds:list):
        """Bulk cancel orders by client ID"""
        r = await self.client.delete(
            "/bulk_orders_by_client_id",
            data={"clientOrderIds": clientOrderIds}
        )
        data = await r.json()
        return data["result"]