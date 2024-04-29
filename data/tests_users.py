from requests import *

print(get("http://localhost:8000/api/Users").json())
print(get("http://localhost:8000/api/Users/1").json())
print(post("http://localhost:8000/api/new_user", json={'name': "Arina", "surname": "Lotosvili", "about": "qwerty", "email":  "arinalotoshili@yandex.ru",
                                                      "hashed_password": "cap"}).json())

print(put("http://localhost:8000/api/user/change_password",  json={"old_password": "cap", "new_password": "cap1", "email": "arinalotoshili@yandex.ru"}).json())
print(put("http://localhost:8000/api/user/change_info", json={"name": "Arina1", "surname": "Lotoshvili1",
                                                              "about": "sdfasdfaassd",
                                                              "email": "arinalotoshili@yandex.ru"}).json())
print(delete("http://localhost:8000/api/del_user/3").json())