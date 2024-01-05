
import random
import json

import aiofiles
import aiohttp
import asyncio


threads = 20

semaphore = asyncio.Semaphore(threads)


def load_proxy():
    with open('proxy.txt', 'r') as f:
        proxy = f.read().splitlines()
    return proxy

async def chech_airdrop(wallet, proxy=None):
    async with semaphore:
        url = f"https://np-api.newparadigm.manta.network/getPointsV1"
        data = {"address":f"{wallet}","polkadot_address":""}
        for i in range(3):
            try:
                print(i)
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=data, proxy=proxy, ssl=False) as response:
                        resp = await response.json()
                        print(resp)
                        if resp['status'] and resp['data']['total_score'] > 0:
                            async with aiofiles.open('manta.txt', 'a') as f:
                                await f.write(json.dumps({'wallet': wallet, 'response': resp}) + '\n')
                            return {'wallet': wallet, 'response': resp}
                        else:
                            break
            except Exception as e:
                print(e)
                continue

async def main():
    tasks = []
    proxy = load_proxy()
    with open('wallets.txt', 'r') as f:
        lines = f.read().splitlines()
        for row in lines:
            address = row[0].strip()
            tasks.append(chech_airdrop(address, proxy=f'http://{random.choice(proxy)}'))

    await asyncio.gather(*tasks)

asyncio.run(main())
