from pony.orm import *
db = Database()


class Links(db.Entity):
    id = PrimaryKey(int, auto=True)
    link = Required(str)
    md5 = Required(str, unique=True)
    state = Required(int)


db.bind(provider='sqlite', filename='links.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
