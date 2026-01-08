import sqlite3


def provjera(imeTablice):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("select * from " + imeTablice)
    if len(cur.fetchall()) > 0:
        conn.close()
        return True
    else:
        conn.close()
        return False
