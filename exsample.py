import asyncio
from pybottersWrap.pybottersFTX import pybottersFTX


async def main(ftx:pybottersFTX):
    async with ftx:
        data = ftx.websocket.set_datastores_endpoint()
        subscribe = ftx.websocket.set_subscribe(["orders","orderbook","fills"], markets=[ftx.pair])
        wstask, store = await ftx.websocket.ws_init(ftx.client,data,subscribe)

        market = await ftx.markets.get_markets()
        print(market)
        

ftx = pybottersFTX("","BTC","JPY")

asyncio.run(main(ftx))

