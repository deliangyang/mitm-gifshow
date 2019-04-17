from pony.orm import *
db = Database()


class GifShowUser(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required(str, unique=True)
    username = Required(str, unique=True)
    gender = Required(int)
    photo = Required(int)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
