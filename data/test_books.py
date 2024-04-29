from requests import *

# print(get("http://localhost:8000/api/books").json())
# print(get("http://localhost:8000/api/book/1").json())
# print(delete("http://localhost:8000/api/del_book/2").json())
print(put("http://localhost:8000//api/jobs/put",
          json={"title": "ЕГЭ.17", "author": "ЕГЭ", "time_for_reading": 2, "about": "asddfasdfasdff1`12221",
                "email": "Nagibimi@gmail.com"}).json())
