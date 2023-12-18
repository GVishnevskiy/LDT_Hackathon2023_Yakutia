from abc import ABC, abstractmethod
from vkbottle import API
import pprint
import json
import asyncio
import typing

from config import VK_LOGIN, VK_PASSWORD

MY_VK_ID = "347307331"
OUTPUT_PATH = r"../output/"
TOKEN = "vk1.a.aSiTJJWP9JyK2YZmPncJ_k0cAmdKNZZRsu6OzXBs7yMxsxFZ-24QIb4astVcRUos7MNser2Nu2wC5mFuu5ARscepK8TI_fmiGpel-dUYd1ePJUcYS_kcig4IR0W7B2KxyXTSyY3rzh399YBTCCW-NYJTRxa_AS16qKZraEisVDDdqhOpJX__l_BUtdbYQWFeW-O5VM4M_ANxT_rNzshJow"
GROUPS_LIMIT = 2
NOTES_LIMIT = 2
KATE_MOBILE = 2685278
GROUP_ACESS_RIGHTS = 262144


class AuthException(Exception):
    pass


class GetUserExeption(Exception):
    pass


class AbstractParser(ABC):
    @abstractmethod
    def parse_one(self, *args, **kwargs):
        ...


class Writer:
    @staticmethod
    def json(data: dict, file_path="groups_discription.txt"):
        with open(OUTPUT_PATH + file_path, 'a', encoding='utf8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    # def db(data: typing.Dict[int, typing.Dict], db: Database):
    #     for user_id, user_groups in data.items():
    #         db.add_vk_user(int(user_id))
    #
    #         groups = Writer.clear_groups(user_groups)
    #         db.add_vk_groups(groups)

    @staticmethod
    def clear_groups(user_groups):
        g = []
        for group_id, group_info in user_groups.items():
            g.append((group_id, group_info["name"], group_info["description"]))
        return g


class VkParser(AbstractParser):
    def __init__(self, token, login=VK_LOGIN):
        self.vk = API(token)

    async def parse_one(self, vk_id):
        await self._check_if_user_exists(vk_id=vk_id)

        user_notes = await self._parse_one_person_notes(vk_id=vk_id)

        groups_ids = await self._parse_one_person_groups(vk_id=vk_id)
        groups_discription = await self._get_groups_description(groups_ids)

        return {vk_id: {"groups": groups_discription, "notes": user_notes}}

    async def _parse_one_person_groups(self, vk_id):
        response = await self.vk.groups.get(user_id=vk_id)
        return response.items[0:GROUPS_LIMIT]

    async def _parse_one_person_notes(self, vk_id):
        response = await self.vk.fave.get(item_type='post', count=NOTES_LIMIT)
        notes = {}
        for note in response.items:
            id = note.post.id
            text = note.post.text
            notes[id] = text
        return notes

    async def _get_groups_description(self, groups_ids: []):
        response = await self.vk.groups.get_by_id(group_ids=groups_ids, fields=["name", "description"])
        groups_description = {}
        for group in response:
            id = group.id
            name = group.name
            description = group.description
            groups_description[id] = {"name": name, "description": description}
        return groups_description

    async def _check_if_user_exists(self, vk_id):
        try:
            await self.vk.users.get(user_ids=vk_id)
        except Exception:
            raise GetUserExeption()


def get_acess_token():
    base_url = f"https://oauth.vk.com/authorize?client_id={KATE_MOBILE}"

    url_params = {
        "redirect_uri": "close.html",
        "display": "page",
        "scope": GROUP_ACESS_RIGHTS,
        "response_type": "token",
    }
    param_url = ""
    for key, value in url_params.items():
        param_url += f"&{key}={value}"

    return base_url + param_url


async def main():
    vk_parser = VkParser(token=TOKEN)
    data = await vk_parser.parse_one(vk_id=MY_VK_ID)
    pprint.pprint(data)


if __name__ == "__main__":
    asyncio.run(main())
