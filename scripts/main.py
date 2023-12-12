from abc import ABC, abstractmethod
import vk_api
import selenium
import pprint
import json
import sqlite3

from config import VK_LOGIN, VK_PASSWORD

MY_VK_ID = "56757868"
OUTPUT_PATH = r"../output/"
TOKEN = "vk1.a.3th8ECvivwyx86YdlsIL69Fdkj2vITUKzATtXJmip0or7v-NRFYdh9lYaPPTCzFH2nnL2RS0ldQMQpQgvCYEsIgYJnSgfNtpcTNrZ5d0rZoarIoWMVjfDt2Ingj2-hw-Y3eCACUFl51ivFSAY2AgV6wEAZXM1dT03WkotoX_pBAiDIZ_IZ0CTeWvXi17-CSpaOSPSRF4gsm_4afFkCIwFw&expires_in=86400"

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
        with open(OUTPUT_PATH+file_path, 'a', encoding='utf8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


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


class VkParser(AbstractParser):
    def __init__(self, login, password):
        vk_session = vk_api.VkApi(token=TOKEN, app_id=2685278)

        vk_session.auth(token_only=True)


        self.vk = vk_session.get_api()
        self.users = {}

    def parse_one(self, vk_id):
        self._check_if_user_exists(vk_id=vk_id)

        groups_ids = self._parse_one_person_groups(vk_id=vk_id)
        groups_discription = self._get_groups_description(groups_ids)

        return {vk_id: groups_discription}

    def _parse_one_person_groups(self, vk_id):
        response = self.vk.groups.get(user_id=vk_id)
        groups = response["items"]
        return groups

    def _get_groups_description(self, groups_ids: []):
        response = self.vk.groups.getById(group_ids=groups_ids, fields="name, description")
        groups_description = {}
        for group in response:
            id = group["id"]
            name = group["name"]
            description = group["description"]
            groups_description[id] = {"name": name, "description": description}
        return groups_description

    def _check_if_user_exists(self, vk_id):
        try:
            self.vk.users.get(user_ids=vk_id)
        except Exception:
            raise GetUserExeption()


def main():
    vk_parser = VkParser(login=VK_LOGIN, password=VK_PASSWORD)
    data = vk_parser.parse_one(vk_id=MY_VK_ID)

    #db = Database(name="vk_users.db")

if __name__ == "__main__":
    main()
