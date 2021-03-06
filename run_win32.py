from selenium import webdriver
import time
from create_db import GifShowUser
from create_links import Links
from pony.orm import *
import random
import platform
import hashlib


@db_session
def update_urls_state(md5):
    try:
        lk = Links.get(md5=md5)
        lk.state = 1
        commit()
    except Exception as e:
        print(e)
        pass


@db_session
def update_urls(url):
    try:
        m2 = hashlib.md5()
        m2.update(url.encode('utf-8'))
        md5 = m2.hexdigest()
        Links(link=url, md5=md5, state=0)
        commit()
    except Exception as e:
        print(e)
        pass


with open('urls.txt', 'r') as fw:
    for line in fw.readlines():
        update_urls(line)


def get_urls():
    for link in Links.select(lambda p: p.state == 0).order_by(Links.id.asc):
        yield (link.link, link.md5)


@db_session
def run(dr):
    for url in get_urls():
        link, md5 = url
        print('current url:%s' % link)
        dr.get(link)
        update_urls_state(md5)
        time.sleep(1)

        for i in range(30):
            print('current: %d' % i)
            js = 'window.scrollBy(%d,%d)' % (2 * i, 1000 * i)
            dr.execute_script(js)
            time.sleep(.1)

        users = GifShowUser.select(
            lambda p: p.gender == 0 and p.photo == 0).order_by(
            GifShowUser.id.asc
        )[:300]
        for user in users:
            print('https://live.kuaishou.com/profile/' + user.username)
            dr.get('https://live.kuaishou.com/profile/' + user.username)
            time.sleep(random.randint(3, 10) / 10)

    while True:
        users = GifShowUser.select(
            lambda p: p.gender == 0 and p.photo == 0).order_by(
            GifShowUser.id.asc
        )[:300]
        if len(users) <= 0:
            break
        for user in users:
            url = 'https://live.kuaishou.com/profile/' + user.username
            print('get: %s' % url)
            dr.get(url)
            js = 'window.scrollBy(%d,%d)' % (random.randint(0, 20), random.randint(980, 2020))
            dr.execute_script(js)
            time.sleep(random.randint(3, 10) / 10)
    dr.close()


def get_chrome_driver():
    os = platform.system()
    if os != 'Darwin':
        return './chromedriver.exe'
    return './chromedriver'


if __name__ == '__main__':
    driver = get_chrome_driver()
    _dr = webdriver.Chrome(executable_path=driver)
    run(_dr)
