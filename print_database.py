import sqlite3

conn = sqlite3.connect('database.sqlite3')
res = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
cur = conn.cursor()
for name in res:
    print(name[0].upper())
    result = cur.execute("select * from {0}".format(name[0])).fetchall()
    for des in cur.description:
        print(des[0] + '  ', end='')
    print('\n----------results :')
    for x in result:
        print(x)
    print('done\n')

conn.close()