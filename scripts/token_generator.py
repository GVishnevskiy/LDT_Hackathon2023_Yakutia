import vk
from config import VK_LOGIN, VK_PASSWORD
from time import sleep

for i in range(900):
    api = vk.UserAPI(
        user_login=VK_LOGIN,
        user_password=VK_PASSWORD,
        scope='offline,wall',
        v='5.131'
    )
    if i % 5 == 0:
        sleep(10)





