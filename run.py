import responder
import datetime as dt
import urllib
import jaconv

import app as backapp
import data as backdata

api = responder.API(static_dir='./static', templates_dir='./static')
api.add_route('/', static=True)
backapp.arrange_db()

@api.route('/roomon')
def roomonperiod(req, resp):
    def urlparams(params, name):
        p = params.get(name, '')
        if not p.isdigit() and p != '-1':
            try:
                if name == 'term':
                    return backdata.term_str(urllib.parse.unquote(p))
                elif name == 'weekday':
                    return backdata.weekday_str(urllib.parse.unquote(p))
            except:
                return -1
        p = int(jaconv.z2h(p, digit=True, ascii=True))
        if p != -1:
            return p
        else:
            if name == 'term':
                return backdata.term_int(dt.datetime.now().date())[0]
            elif name == 'weekday':
                return dt.datetime.now().weekday()
            elif name == 'period':
                return backdata.period_int(dt.datetime.now())[0]
    resp.media = backapp.rooms_on(*[urlparams(req.params, name) for name in ['term', 'weekday', 'period']])

if __name__ == "__main__":
    api.run()