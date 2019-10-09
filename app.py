from database import *

def freerooms_on(day, period):
    with SessionContext() as session:
        return [r for r in room_names() if eval(f'data.{r}', {}, {
            'data': session.query(FreeRooms).filter_by(day_period=f'{day}_{period}').one()
        }) == 0]

def fetch_classinfo(class_id):
    if class_id == 0:
        return None
    with SessionContext() as session:
        return session.query(ClassInfo).get(class_id)

def used_on(room_name):
    with SessionContext() as session:
        return {t[0]: l[0] for t, l in zip(
            eval(f'session.query(FreeRooms.day_period)'),
            eval(f'session.query(FreeRooms.{room_name})')
        )}

def is_free(room_name, day, period):
    return room_name in freerooms_on(day, period)

def arrange_db():
    for n in engine.execute('select * from freerooms')._metadata.keys[2:]:
        FreeRooms.add_field(n, Integer)

def room_names():
    return FreeRooms.__table__.columns.keys()[2:]

if __name__ == "__main__":
    arrange_db()
    print(freerooms_on(0, 2))
    print(room_names())
    print(is_free('r03_601', 0, 2))
