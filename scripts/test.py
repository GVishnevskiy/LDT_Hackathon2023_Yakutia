# from pprint import pprint
#
# s = {30602036: {'name': 'IGM', 'description': 'Самое крупное игровое сообщество на просторах СНГ ಠಿ_ಠ'}, 93893399: {'name': 'GabeStore', 'description': 'Официальное сообщество интернет-магазина GabeStore. Помогаем геймерам покупать игры дешевле.\n\nПо любым вопросам к магазину обращайтесь в сообщения группы.\nТехподдержка работает круглосуточно, без выходных.'}, 159146575: {'name': 'Мемуары ценителей научных мемов', 'description': 'Познавательные мемы, широкий охват тем, уникальные идеи и оригинальное оформление. Наскучил однотипный контент? Тогда вы по адресу :)\n\nTelegram: https://t.me/memoirs_exclusive'}, 161516291: {'name': 'Афиша.Онлайн - Москва', 'description': 'Кино, концерты, шоу, спорт, клубы и фестивали.'}, 120254617: {'name': '$$$ DANK MEMES $$$ AYY LMAO $$$', 'description': 'TRUE SHIT FROM TUMBLR AND REDDIT'}, 170567511: {'name': 'Карельский бальзам', 'description': 'Сообщество Карельский бальзам посвящено деятельности стримера-политолога из Петрозаводска Владислава Дмитриевича Жмилевского (aka Жмиль)'}, 72378974: {'name': 'Мой Компьютер', 'description': 'МК - сообщество, посвященное компьютерам и IT. \nРедакция МК ежедневно публикует самые интересные новости из мира высоких технологий и науки. \n\nМы Telegram - https'}}
#
# ans = []
# for group_id, group_info in s.items():
#     ans.append((group_id, group_info["name"], group_info["description"]))
#
#
# pprint(ans)


users = [
    ("James", 25, "male", "USA"),
    ("Leila", 32, "female", "France"),
    ("Brigitte", 35, "female", "England"),
    ("Mike", 40, "male", "Denmark"),
    ("Elizabeth", 21, "female", "Canada"),
]

user_records = ", ".join(["{}"] * len(users))

insert_query = (
    f"INSERT INTO users (name, age, gender, nationality) VALUES {user_records}"
)

print(insert_query.format(*users))


a = 21

pek = {a : ([1], [2])}

print(pek)