from create_db import GifShowUser
from pony.orm import *
from xlwt import *


@db_session()
def export(filename, gender, photo):
    start = 0
    ws = Workbook(encoding='utf-8')
    w = ws.add_sheet('sheet1')
    row = 0
    while True:
        s = GifShowUser.select(
            lambda p: p.id > start).where(
            lambda p: p.gender == gender)
        if photo <= 0:
            s = s.where(lambda p: p.photo <= 0)
        else:
            s = s.where(lambda p: p.photo > 0)
        users = s.order_by(
            GifShowUser.id.asc
        )[:300]
        if len(users) <= 0:
            break
        for user in users:
            start = user.id
            w.write(row, 0, user.user)
            w.write(row, 1, user.username)
            row += 1
    ws.save(filename)


def main():
    export(r'./data/女无.xlsx', 2, 0)
    export(r'./data/女有.xlsx', 2, 1)
    export(r'./data/男无.xlsx', 1, 0)
    export(r'./data/男有.xlsx', 1, 1)


if __name__ == '__main__':
    main()
    print('done')
