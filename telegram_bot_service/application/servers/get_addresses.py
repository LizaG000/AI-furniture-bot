import aiohttp
import json
from typing import Tuple
from presentation.handlers.addresses.schemas import AddressSchema, adapter
from application.data.users import users

async def get_addresses_list(id_user: int, chat_id: int) -> Tuple[str, list[str], list[AddressSchema]]:
    async with aiohttp.ClientSession() as session:
        params={'id_user': str(id_user)}
        result = await session.get('http://future-backend.tw1.ru:8003/api/address', params=params)
        print(await result.text())
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
        users[id_user]["text"] = text
        users[id_user]["addresses"] = addresses
        users[id_user]["results"] = results

        return text, addresses, results
