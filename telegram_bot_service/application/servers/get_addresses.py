import aiohttp
import json
from pydantic import types
from presentation.handlers.addresses.schemas import AddressSchema, adapter


async def get_addresses_list(id_user: int) -> types[str, list[str], list[AddressSchema]]:
    async with aiohttp.ClientSession() as session:
        params={'id_user': str(id_user)}
        result = await session.get('http://future-backend.tw1.ru:8003/api/address', params=params)
        results = adapter.validate_python(json.loads(await result.text()))
        addresses  = []
        for i in results:
            string = ""
            string += "Страна: " + i.country + "\n"
            string += "Регион: " + i.region + "\n"
            string += "Город: " + i.city + "\n"
            string += "Улица: " + i.street + "\n"
            string += "Номер дома: " + i.house_number + "\n"
            string += "Номер квартиры: " + i.quadrature_number + "\n"
            string += "Почтовый индекс: " + str(i.postal_code) + "\n"
            addresses.append(string)
                  
        text = "\n".join(f"{i+1}. {address}" for i, address in enumerate(addresses))
        return text, addresses, results
