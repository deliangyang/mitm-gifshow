from selenium import webdriver
import time
from create_db import GifShowUser
from pony.orm import *
import random
dr = webdriver.Chrome(executable_path="./chromedriver")

start = 0
with open('flag', 'r') as f:
    start = f.read() or 0
    f.close()


def get_urls():
    with open('urls', 'r') as fw:
        for line in fw:
            yield line


@db_session
def run():
    for url in get_urls():
        print('current url:%s' % url)
        dr.get(url)
        time.sleep(1)

        for i in range(30):
            print('current: %d' % i)
            js = 'window.scrollBy(%d,%d)' % (2 * i, 1000 * i)
            dr.execute_script(js)
            time.sleep(1)

        users = GifShowUser.select(
            lambda p: p.id > start).order_by(
            GifShowUser.id.asc
        )[:300]
        for user in users:
            dr.get('https://live.kuaishou.com/profile/' + user.username)
            start = user.id
            with open('flag', 'w') as fw:
                fw.write(start)
                fw.close()
            time.sleep(1)
        time.sleep(1)

    while True:
        users = GifShowUser.select(
            lambda p: p.id > start).order_by(
            GifShowUser.id.asc
        )[:300]
        if len(users) <= 0:
            break
        for user in users:
            url = 'https://live.kuaishou.com/profile/' + user.username
            print('get: %s' % url)
            dr.get(url)
            start = user.id
            with open('flag', 'w') as fw:
                fw.write(start)
                fw.close()
            js = 'window.scrollBy(%d,%d)' % (random.randint(0, 20), random.randint(980, 1020))
            dr.execute_script(js)
            time.sleep(1)
    dr.close()


if __name__ == '__main__':
    run()
