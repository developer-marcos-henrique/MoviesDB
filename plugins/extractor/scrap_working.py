from bs4 import BeautifulSoup
import aiohttp, asyncio, json



class scrap_handler:
    def __init__(self, search: str):
        self.search = search
        self.results = list()

        self.websites_without_automation_part1 = {
            "animefire": {
                "url": "https://animefire.plus/proc/quicksearch", 
                "method": "POST",
                "headers": {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"},
                "data": {"word": search},
                "params": {},
                "wordPressDefault": True,
                "browser_mode": False
            },
            
            "goyabu": {
                "url": "https://goyabu.to/wp-json/animeonline/search/?",
                "method": "GET",
                "headers": {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"},
                "data": {},
                "params": {"keyword": search, "nonce": "5ecb5079b5"},
                "wordPressDefault": False,
                "browser_mode": False
            },    
            
            "animesbr": {
                "url": "https://animesbr.tv/?",
                "method": "GET",
                "headers": {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"},
                "data": {},
                "params": {"s": search},
                "wordPressDefault": False,
                "browser_mode": False
            }
        } 
            
        self.websites_without_automation_part2 = {
            "aniwatch": {
                "url": "https://aniwatchtv.to/ajax/search/suggest?",
                "method": "GET",
                "headers": {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"},
                "data": {},
                "params": {"keyword": search},
                "wordPressDefault": False,
                "browser_mode": False
            },     
            
            "9animetv": {
                "url": "https://9animetv.to/search?",
                "method": "GET",
                "headers": {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"},
                "data": {},
                "params": {"keyword": search},
                "wordPressDefault": False,
                "browser_mode": False
            }
        }

        self.websites_with_normal_automation = {}
        

        self.websites_with_custom_automation = {
            "kissanime": {
                "url": "https://kissanime.com.ru/Search/?",
                "method": "GET",
                "headers": {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"},
                "data": {},
                "params": {"s": search},
                "wordPressDefault": False,
                "browser_mode": True
            }
        }

    async def run(self):
        #await self.playwrightAutomation()

        tasks = [
            asyncio.create_task(self.beautifulscrap(obs=self.websites_without_automation_part1)),
            asyncio.create_task(self.beautifulscrap(obs=self.websites_without_automation_part2))
        ]
        
        await asyncio.gather(*tasks)

        
        return self.results

    async def beautifulscrap(self, obs: dict, proxy=None, auth=None) -> list:        
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(3), proxy=proxy, auth=None) as requests:
            for obj in obs.items():
                await asyncio.sleep(0.1)

                if obj[1]['method'] == "POST":
                    request_obj = await requests.post(
                        url=obj[1].get("url"),
                        data=obj[1].get("data"),
                        params=obj[1].get("params"),
                        headers=obj[1].get("headers")
                        )
                
                else:
                    request_obj = await requests.get(
                        url=obj[1].get("url"),
                        data=obj[1].get("data"),
                        params=obj[1].get("params"),
                        headers=obj[1].get("headers")
                        )
                

                if request_obj.status == 200:
                    
                    try:
                        self.results.append((obj[0], json.loads(await request_obj.text())))
                    
                    except json.JSONDecodeError:
                        self.results.append((obj[0], await request_obj.text()))
