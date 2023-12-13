from abc import ABC, abstractmethod
from vkbottle import API
import selenium
import pprint
import json
import sqlite3
import asyncio
import typing

from config import VK_LOGIN, VK_PASSWORD

MY_VK_ID = "347307331"
OUTPUT_PATH = r"../output/"
TOKEN = "vk1.a.eDiyffPjcbtyqySj_PULS_KtdvjjO1NmM9SRJq4G1r4kVMyQeIcYz72Ub0V1lFkwtZ1wMWv0m-j8mv-RQnzzYOKEB9JcIEwPCALIn3IUI6ft7ubFnaZXNw49byWT0ccN8PXmbu59FQ3_dH6xl9j44uLgoceNWHS5XIXxEQzGDSILTvR2Kf86mu7Qo3OfeRkTkpP3xwtVIUEfnpKEEKTHIw"
GROUPS_LIMIT = 2
NOTES_LIMIT = 2


class AuthException(Exception):
    pass


class GetUserExeption(Exception):
    pass


class AbstractParser(ABC):
    @abstractmethod
    def parse_one(self, *args, **kwargs):
        ...


class DBQueries:
    add_vk_user = """
    INSERT INTO 
        vk_users (id)
    VALUES 
        ({0})
    """

    add_vk_group = """
    INSERT INTO 
        vk_groups (id, group_name, group_description)
    VALUES 
        {}
    """

    bind_user_group = """
    
    """


class Database:
    def __init__(self, name):
        self._conn = sqlite3.connect(OUTPUT_PATH + name)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def add_vk_user(self, user_id):
        q = DBQueries.add_vk_user.format(user_id)
        print(q)

    def add_vk_groups(self, groups):
        filler = ", ".join(["{}"] * len(groups))
        q = DBQueries.add_vk_group.format(filler)

        g = []
        for group_id, group_info in groups.items():
            g.append((group_id, group_info["name"], group_info["description"]))

        print(q.format(*g))


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


async def main():
    db = Database(name="vk_users.db")

    vk_parser = VkParser(token=TOKEN)
    data = await vk_parser.parse_one(vk_id=MY_VK_ID)
    print(data)


if __name__ == "__main__":
    asyncio.run(main())
