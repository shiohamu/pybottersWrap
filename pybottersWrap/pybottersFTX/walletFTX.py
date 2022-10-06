import pybotters

class walletFTX:

    def __init__(self,ticker,asset,pair,client:pybotters.Client):
        self.client = client
        self.ticker = ticker
        self.asset = asset
        self.pair = pair

    ################## Wallet ################## 


    async def get_coins(self):
        """get coins"""
        r = await self.client.get(
            "/wallet/coins"
        )
        data = await r.json()
        return data["result"]

    async def get_balances(self):
        """get balances"""
        r = await self.client.get(
            "/wallet/balances"
        )
        data = await r.json()
        return data["result"]

    async def get_balances_all_accounts(self):
        """get balances all accounts\n
        The response will contain an object whose keys are the subaccount names. The main account will appear under the key main.
        """
        r = await self.client.get(
            "/wallet/all_balances"
        )
        data = await r.json()
        return data["result"]

    async def get_deposit_address(self,coin=None,method=None):
        """get deposit address"""
        if coin == None: coin = self.asset
        params = None
        if method != None: params = {"method": method}
        r = await self.client.get(
            "/wallet/deposit_address",
            params=params
        )
        data = await r.json()
        if data["success"] == True:
            return data["result"]
        else:
            return data["success"]

    async def get_deposit_address_list(self,coin=None,method=None):
        """get deposit address list"""
        if coin == None: coin = self.asset
        params = None
        if method != None: params = [{"coin": coin, "method": method}]
        else: params = [{"coin": coin}]
        r = await self.client.post(
            "/wallet/deposit_address/list",
            data=params
        )
        data = await r.json()
        if data["success"] == True:
            return data["result"]
        else:
            return data["success"]

    async def get_deposit_history(self,page=None):
        """get deposit history"""
        params = None
        if page != None: params = page
        r = await self.client.get(
            "/wallet/deposits",
            params = params
        )
        data = await r.json()
        return data["result"]
    
    async def get_withdrawal_history(self,page=None):
        """get withdrawal history"""
        params = None
        if page != None: params = page
        r = await self.client.get(
            "/wallet/withdrawals",
            params=params
        )
        data = await r.json()
        return data["result"]

    async def request_withdrawal(self,size,address,coin,tag=None,method=None,password=None,code=None):
        """request withdrawal"""
        if coin == None: coin = self.pair
        params =    {"coin": coin,
                    "size": size,
                    "address": address}
        if tag != None: params.setdefault("tag", tag)
        if method != None: params.setdefault("method", method)
        if password != None: params.setdefault("password", password)
        if code != None: params.setdefault("code", code)

        r = await self.client.post(
            "/wallet/withdrawals",
            data=params
        )
        data = await r.json()
        return data["result"]


    async def get_airdrops(self,page=None):
        """get airdrops\n
        This endpoint provides you with updates to your AMPL balances based on AMPL rebases.
        """
        params = None
        if page != None: params = page
        r = await self.client.get(
            "/wallet/airdrops",
            params=params
        )
        data = await r.json()
        return data["result"]

    async def get_withdrawal_fees(self,coin,size,address,tag=None,method=None):
        """get withdrawal fees"""
        params =    {"coin": coin,
                    "size": size,
                    "address": address}
        if tag != None: params.setdefault("tag", tag)
        if method != None: params.setdefault("method", method)
        r = await self.client.get(
            "/wallet/withdrawal_fee",
            params=params
        )
        data = await r.json()
        return data["result"]

    async def get_saved_addresses(self,coin):
        """get saved  addresses\n
        This endpoint provides you with your saved addresses
        """
        params = {"coin": coin}
        r = await self.client.get(
            "/wallet/saved_addresses",
            params=params
        )
        data = await r.json()
        return data["result"]

    async def create_saved_address(self,coin,address,wallet,addressName,isPrimetrust,tag=None,whitelist=None,code=None):
        """create saved address"""
        params =    {"coin": coin,
                    "address": address,
                    "wallet": wallet,
                    "addressName": addressName,
                    "isPrimetrust": isPrimetrust}
        if tag != None: params.setdefault("tag", tag)
        if whitelist != None: params.setdefault("whitelist", whitelist)
        if code != None: params.setdefault("code", code)
        r = await self.client.post(
            "/wallet/saved_addresses",
            data=params
        )
        data = await r.json()
        return data["result"]

    async def delete_saved_address(self,saved_address_id):
        """delete saved address"""
        r = await self.client.delete(
            "/wallet/saved_addresses/{}".format(saved_address_id)
        )
        data = await r.json()
        return data["result"]

    async def register_SEN_deposit(self,sen_link_id,size):
        """register a SEN deposit\n
        Register a SEN deposit within our system. In order to be auto-credited, you must register the deposit with us beforehand.
        """
        r = await self.client.post(
            "/sen/deposits/{}".format(sen_link_id),
            data={"size": size}
        )
        data = await r.json()
        return data["result"]

    async def register_signet_deposit(self,signet_link_id,size):
        """register a Signet deposit"""
        r = await self.client.post(
            "/signet/deposits/{}".format(signet_link_id),
            data={"size": size}
        )
        data = await r.json()
        return data["result"]

    async def request_signet_withdrawal(self,signet_link_id,size):
        """request a Signet withdrawal"""
        r = await self.client.post(
            "/signet/withdrawal/{}".format(signet_link_id),
            data={"size": size}
        )
        data = await r.json()
        return data["result"]