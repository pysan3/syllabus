from database import *

def rooms_on(term, day, period):
    with SessionContext() as session:
        data = session.query(FreeRooms).filter_by(term=term, day_period=f'{day}_{period}').one_or_none()
        if data is None:
            return {r: 0 for r in room_names()}
        return {r: eval(f'data.{r}', {}, {'data': data}) for r in room_names()}

def fetch_classinfo(class_id):
    if class_id == 0:
        return None
    with SessionContext() as session:
        return session.query(ClassInfo).get(class_id)

def used_on(room_name):
    with SessionContext() as session:
        return [{t[0]: l[0] for t, l in zip(
            eval(f'session.query(FreeRooms.day_period).filter_by(term=i)'),
            eval(f'session.query(FreeRooms.{room_name}).filter_by(term=i)')
        )} for i in range(4)]

def is_free(room_name, term, day, period):
    return rooms_on(term, day, period)[room_name] == 0

def arrange_db():
    for n in engine.execute('select * from freerooms')._metadata.keys[3:]:
        FreeRooms.add_field(n, Integer)

def room_names():
    return FreeRooms.__table__.columns.keys()[3:]

if __name__ == "__main__":
    arrange_db()
    print(freerooms_on(0, 2))
    print(room_names())
    print(is_free('r03_601', 0, 2))
