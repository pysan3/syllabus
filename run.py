import responder
import datetime as dt

import app as backapp
import data as backdata

api = responder.API(static_dir='./static', templates_dir='./static')
api.add_route('/', static=True)
backapp.arrange_db()

@api.route('/roomon')
def roomonperiod(req, resp):
    def urlparams(params, name):
        p = params.get(name, '')
        if p != -1:
            return p
        return {
            'term': backdata.term(dt.datetime.now().date())[0],
            'weekday': dt.datetime.now().weekday(),
            'period': backdata.period(dt.datetime.now())[0]
        }[name]
    resp.media = backapp.rooms_on(*[urlparams(req.params, name) for name in ['term', 'weekday', 'period']])

if __name__ == "__main__":
    api.run()