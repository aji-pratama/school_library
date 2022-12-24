# Simple Library

## Installation

1. Run Pip install: `pip install -r requirements.txt`
2. Run migration: `python3 manage.py migrate`
3. Load Fixtures: `python3 manage.py loaddata fixture/library.json` *Fixture data is include: user, userrole, book. borrow is not included
4. Running Unittest: `python3 manage.py test`


## User Credentials:

1. Admin:
    - username: `admin`
    - pass: `password999`

2. Student:
    - username: `student`
    - pass: `password999`

3. Librarian:
    - username: `librarian`
    - pass: `password999`


### API:

|No |Method|Endpoint                                           |
|---|------|---------------------------------------------------|
|1. |`GET` |`127.0.0.1:8000/library/books/`                    |
|2. |`GET` |`127.0.0.1:8000/library/borrow/`                   |
|3. |`PUT` |`127.0.0.1:8000/library/borrow/renew/<int:pk>/`    |
|4. |`GET` |`127.0.0.1:8000/library/borrow/history/`           |
|5. |`GET` |`127.0.0.1:8000/library/librarian-borrow/`         |
|6. |`GET` |`127.0.0.1:8000/library/librarian-borrow/<int:pk>/`|
|7. |`POST`|`127.0.0.1:8000/library/borrow/<int:pk>/`          |
|8. |`PUT` |`127.0.0.1:8000/library/borrow/return/<int:pk>/`   |
