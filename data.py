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

if __name__ == "__main__":
    print(period(dt.datetime.now()))
