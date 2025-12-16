import asyncio
import json
import websockets
from datetime import datetime
from storage import insert_tick

_running = False

async def _listen_symbol(symbol):
    url = f"wss://fstream.binance.com/ws/{symbol}@trade"
    async with websockets.connect(url) as ws:
        while _running:
            try:
                msg = await ws.recv()
                data = json.loads(msg)

                ts = datetime.utcfromtimestamp(data["T"] / 1000).isoformat()
                insert_tick(ts, symbol, float(data["p"]), float(data["q"]))
            except:
                break

async def start_stream(symbols):
    global _running
    _running = True
    await asyncio.gather(*[_listen_symbol(s) for s in symbols])

def stop_stream():
    global _running
    _running = False
