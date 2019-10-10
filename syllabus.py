from selenium import webdriver
from selenium.webdriver.support.ui import Select
import numpy as np
import jaconv
from time import sleep

from database import *

gakubu = {
    'kikan': '262006',
    'souzou': '272006',
    'senshin': '282006'
}

def get_class(gakubu_key, max_search=None):
    driver.get('https://www.wsl.waseda.jp/syllabus/JAA101.php')

    # gakubu
    p_gakubu = driver.find_element_by_name('p_gakubu')
    Select(p_gakubu).select_by_value(gakubu_key)
    # search
    driver.find_element_by_name('btnSubmit').click()
    sleep(0.5)

    # get keys of every class
    counter = 1
    info = []
    while True:
        info.extend([class_info(tr) for tr in driver.find_elements_by_xpath('//div[@class="ctable-main"]/table/tbody/tr[not(@class="c-vh-title")]')])

        # go to next page
        if not next_page():
            break

        if counter == max_search:
            break
        counter += 1
    print(f'search for gakubu: "{gakubu_key}" finished with {counter} requests.')

    return [d for d in info if d is not None]

def class_info(tr):
    d = dict()
    yobi = ['月','火','水','木','金','土','日']
    season = ['春', '夏', '秋', '冬']
    for i, td in enumerate(tr.find_elements_by_tag_name('td')):
        try:
            if i == 0:
                d['year'] = int(td.text)
            elif i == 2:
                d['name'] = td.text
                d['key'] = td.find_element_by_tag_name('a').get_attribute('onclick').split("'")[3]
            elif i == 5:
                d['term'] = '0123' if td.text == '通年' else str(season.index(td.text[0]))
                if td.text[1:] == '学期':
                    d['term'] += f'{int(d["term"]) + 1}'
            elif i == 6:
                d['weekday'] = int(yobi.index(td.text[0]))
                d['period'] = int(jaconv.z2h(td.text[1],digit=True,ascii=True))
            elif i == 7:
                info = td.text.split('-')
                if info[0].isdecimal() and (info[1][:3].isdecimal() or info[1][0] == 'B'):
                    d['building'] = int(jaconv.z2h(info[0],digit=True,ascii=True))
                    d['room'] = jaconv.z2h(info[1][:3],digit=True,ascii=True)
                else:
                    raise Exception
        except:
            # print('error on ', tr.text)
            return None
    return d

def next_page():
    for next_page in driver.find_elements_by_class_name('t-btn'):
        for a in next_page.find_elements_by_tag_name('tbody > tr > td > div > div > p > a'):
            if a.text == '次へ>':
                a.click()
                sleep(1)
                return True
    return False

def time2str(weekday, period):
    return f'{weekday}_{period}'
def room2str(building, room):
    return f'r{building:02d}_{room}'

class TimeTable:
    def __init__(self):
        self.time = dict()
        self.timecounter = 0
        self.rooms = dict()
        self.roomcounter = 0
        self.table = np.zeros((0, 0, 4), dtype=int)

    def add(self, term, time, room, class_id):
        if time not in self.time:
            self.table = np.concatenate((
                self.table,
                np.zeros((1, self.roomcounter, 4), dtype=int)
            ), 0)
            self.time[time] = self.timecounter
            self.timecounter += 1
        if room not in self.rooms:
            self.table = np.concatenate((
                self.table,
                np.zeros((self.timecounter, 1, 4), dtype=int)
            ), 1)
            self.rooms[room] = self.roomcounter
            self.roomcounter += 1
        for s in term:
            self.table[self.time[time], self.rooms[room], int(s)] = class_id

def scrape(max_search=None):
    with SessionContext() as session:
        for i in gakubu.values():
            session.execute(ClassInfo.__table__.insert(), get_class(i, max_search))

def database2table(table):
    with SessionContext() as session:
        for c in session.query(ClassInfo).all():
            table.add(c.term, time2str(c.weekday, c.period), room2str(c.building, c.room), c.id)

def create_timedatabase(table):
    for r in sorted(table.rooms.keys()):
        FreeRooms().add_column(r, Integer)

def insert_class_info(table):
    with SessionContext() as session:
        session.execute(FreeRooms.__table__.insert(), [dict({
            room: int(table.table[table.time[t], table.rooms[room], i]) for room in table.rooms.keys()
        }, **{'day_period': t, 'term': i}) for i in range(4) for t in sorted(table.time.keys())])

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    import platform
    if platform.system() == 'Linux':
        driver = webdriver.Chrome(executable_path='/mnt/c/Program Files/chromedriver/chromedriver.exe', options=options)
    else:
        driver = webdriver.Chrome(options=options)

    import sys
    scrape(int(sys.argv[1]) if len(sys.argv) == 2 else None)

    table = TimeTable()
    database2table(table)
    create_timedatabase(table)
    insert_class_info(table)
