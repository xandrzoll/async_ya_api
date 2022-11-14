import asyncio
from aiohttp import ClientSession

from services.config import YA_KEY


BASE_URL_YA_2 = 'https://geocode-maps.yandex.ru/1.x?apikey={}&geocode={}&format=json'


def choose_address(geo_data: dict):
    geos = geo_data['response']['GeoObjectCollection']['featureMember']
    if len(geos) == 1:
        return geos[0]
    request_text = geo_data['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['request']
    for symb in ('.', ',', '-', ':',):
        request_text = request_text.replace(symb, '')

    result = {}
    request_text = request_text.split()
    max_count_match = 0
    for geo in geos:
        response_text = geo['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
        count_match = 0
        for word in request_text:
            if word in response_text:
                count_match += 1
        if count_match > max_count_match:
            max_count_match = count_match
            result = geo
    return result


async def get_geo_coordinates_async(adr, session: ClientSession, sem: asyncio.Semaphore):
    async with sem:
        pos = ''
        try:
            async with session.get(BASE_URL_YA_2.format(YA_KEY, adr)) as resp:
                pos = await resp.json()
                # pos = pos['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
                print(f"{adr} -> {pos['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']}")
                await asyncio.sleep(1)
        except Exception as err:
            print(err)
        return pos


async def process_get_geo_coordinates_async(func, iterator, n=45):
    semaphore = asyncio.Semaphore(n)

    async with ClientSession() as session:
        tasks = []
        for i in iterator:
            tasks.append(
                func(i, session, semaphore)
            )
        results = await asyncio.gather(*tasks)
        return results


# class AsyncRequest:
#     def __init__(self):
#         self.session = ClientSession()
#
#     def close(self):
#         self.session.close()
#
#     async def get(self, url, params=None, content_type='json', *args, **kwargs):
#         if params:
#             url = url.format(params)
#         try:
#             resp = await self.session.get(url, *args, **kwargs)
#             if content_type != 'json':
#                 data = await resp.read()
#             else:
#                 data = await resp.json()
#         except Exception as err:
#             return {'error': err}
#         return data
#
#
#
#     def post(self, url, *args, **kwargs):
#         pass
#
#     def run(self, iterator, max_task=10):
#         result = asyncio.run(
#             self.process(self.method, iterator=iterator, max_task=max_task)
#         )
#         return result
#
#     @staticmethod
#     async def process(method, func, iterator, max_task):
#         semaphore = asyncio.Semaphore(max_task)
#
#         async with ClientSession() as session:
#             tasks = []
#             for i in iterator:
#                 tasks.append(
#                     func(i, session, semaphore)
#                 )
#             results = await asyncio.gather(*tasks)
#             return results
#
#     def method(self):
#         pass
