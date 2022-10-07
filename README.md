# pybottersWrap
pybottersWrapはまちゅけんさん作の[pybotters](https://github.com/MtkN1/pybotters)のラッパークラスです。

pybottersのラッパークラスの作例が見つからなかったため何となく作りました。

読みづらいと思うので、私が使う以外のことは想定していません。

現在FTXのみ、途中までサポートしています。

更新予定はありません。

Pypl登録予定もありません。

### exsample

```python

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

```
