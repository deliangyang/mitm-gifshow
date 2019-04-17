from mitmproxy import http
from mitmproxy import ctx
import json
from pony.orm import *
from create_db import GifShowUser
import re

gender_re = re.compile(r'user-info-sex (female|male)')
photo_re = re.compile(r'<li class="feed-list-item"')

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)


def request(flow: http.HTTPFlow):
    # redirect to different host
    # if flow.request.pretty_host == "live.kuaishou.com":
    #     flow.request.host = "live.kuaishou.com"
    # # answer from proxy
    # elif flow.request.path.endswith("/graphql"):
    #     ctx.log.info(flow.response)
    pass


@db_session
def insert(comment):
    try:
        GifShowUser(
            user=comment['authorId'],
            username=comment['authorEid'],
            gender=0,
            photo=0
        )
        commit()
    except Exception as e:
        print(e)
        ctx.log.error(e)
        pass


@db_session
def user_update(username, gender, photo):
    try:
        user_info = GifShowUser.get(username=username)
        _gender = 0
        if gender == 'female':
            _gender = 2
        elif gender == 'male':
            _gender = 1
        user_info.gender = _gender
        user_info.photo = photo
        commit()
    except Exception as e:
        ctx.log.error(str(e))


def response(flow: http.HTTPFlow) -> None:
    if flow.request.path.endswith('/graphql'):
        try:
            data = json.loads(flow.response.text)
            comments = data['data']['shortVideoCommentList']['commentList']
            for comment in comments:
                insert(comment)
                print((comment['authorId'], comment['authorEid']))
                for subComment in comment['subComments']:
                    insert(comment)
                    print((subComment['authorId'], subComment['authorEid']))
        except Exception as e:
            ctx.log.error(str(e))
            pass
    if flow.request.path.startswith('/profile'):
        gender = gender_re.findall(flow.response.text)
        photo = photo_re.findall(flow.response.text)
        _gender = ''
        if len(gender) > 0:
            _gender = gender[0]

        username = flow.request.path.replace('/profile/', '')
        user_update(username, _gender, len(photo))
