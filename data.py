import datetime as dt

def period(time):
    timetable = (
        (dt.time(9, 0), dt.time(10, 30)),
        (dt.time(10, 40), dt.time(12, 10)),
        (dt.time(13, 0), dt.time(14, 30)),
        (dt.time(14, 45), dt.time(16, 15)),
        (dt.time(16, 30), dt.time(18, 0)),
        (dt.time(18, 15), dt.time(19, 45)),
    )
    for i, t in enumerate(timetable):
        for j, u in enumerate(t):
            if (dt.datetime.combine(dt.date.today(), u) - time).total_seconds() >= 0:
                return i + 1, j

def term(date):
    calender = (
        (dt.date(date.year, 4, 1), dt.date(date.year, 6, 7)),
        (dt.date(date.year, 6, 8), dt.date(date.year, 8, 2)),
        (dt.date(date.year, 9, 21), dt.date(date.year, 11, 26)),
        (dt.date(date.year, 11, 27), dt.date(date.year, 12, 31)),
    )
    if (dt.date(date.year, 2, 4) - date).days >= 0:
        return 3 # 冬学期は年をまたぐので新年後は別処理
    for i, t in enumerate(calender):
        for j, s in enumerate(t):
            if (s - date).days >= 0:
                return i, j

if __name__ == "__main__":
    print(period(dt.datetime.now()))
