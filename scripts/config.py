import os
from dotenv import load_dotenv


load_dotenv()

VK_LOGIN = os.getenv("VK_LOGIN")
VK_PASSWORD = os.getenv("VK_PASSWORD")

MY_VK_ID = "347307331"
OUTPUT_PATH = r"../output/"
TEST_TOKEN = ""
GROUPS_LIMIT = 1
NOTES_LIMIT = 1
KATE_MOBILE = 2685278
GROUP_ACESS_RIGHTS = 262144