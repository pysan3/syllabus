import responder
import datetime as dt

import app as backapp
import data as backdata

api = responder.API(static_dir='./static', templates_dir='./static')
backapp.arrange_db()

@api.route('/freenow')
def freenow(req, resp):
    return {'rooms': backapp.freerooms_on(
        dt.datetime.now().weekday(),
        backdata.period(dt.datetime.now())[0]
    )}

@api.route('/freeonperiod/{period}')
def freeonperiod(req, resp, *, period):
    return {'rooms': backapp.freerooms_on(
        dt.datetime.now().weekday(),
        period
    )}

if __name__ == "__main__":
    api.run()