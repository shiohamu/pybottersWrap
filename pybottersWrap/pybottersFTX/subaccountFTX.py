import pybotters

class subaccountFTX:

    def __init__(self,ticker,asset,pair,client:pybotters.Client):
        self.client = client
        self.ticker = ticker
        self.asset = asset
        self.pair = pair

        ################## Subaccounts ################## 


    async def get_all_subaccounts(self):
        """get all subaccounts"""
        r = await self.client.get(
            "/subaccounts"
        )
        data = await r.json()
        return data["result"]

    async def create_subaccount(self,subaccount):
        """create subaccount"""
        r = await self.client.post(
            "/subaccounts",
            data={"nickname": subaccount}
        )
        data = await r.json()
        return data
        
    async def change_subaccount_name(self,nickname,newNickname):
        """change subaccount name"""
        params = {"nickname": nickname, "newNickname": newNickname}
        r = await self.client.post(
            "/subaccounts/update_name",
            data=params
        )
        data = await r.json()
        return data

    async def delete_subaccount(self,nickname):
        """delete subaccount"""
        params = {"nickname": nickname}
        r = await self.client.delete(
            "/subaccounts",
            data=params
        )
        data = await r.json()
        return data

    async def get_subaccount_balances(self,subaccount=None):
        """get subaccount balances"""
        if subaccount == None: subaccount = self.subaccount
        r = await self.client.get(
            "/subaccounts/{}/balances".format(subaccount)
        )
        data = await r.json()
        return data["result"]
    
    async def get_subaccount_balances_list(self,subaccount=None):
        """get subaccount balances list"""
        data = await self.get_subaccount_balances(subaccount)
        balances = {}
        for i in range(len(data)):
            balances.setdefault(data[i]["coin"], data[i]["free"])
        return balances

    async def transfer_between_subaccounts(self,source, destination):
        """transfer between subaccounts"""
        params = {"source": source, "destination": destination}
        r = await self.client.post(
            "/subaccounts/transfer",
            data=params
        )
        data = r.json()
        return data