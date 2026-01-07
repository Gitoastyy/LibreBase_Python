import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
import sqlite3
kivy.require('2.1.0')

try:
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

except:
    print('DB exists')

class MainWindow(Screen):
    global selector
    selector = ''
    def closure(self):
        conn.close()

    def table_b(self):
        cur.execute("CREATE TABLE IF NOT EXISTS book(name text primary key not null, original text not null, publisher text not null, genre text not null, year text not null)")

    def table_p(self):
        cur.execute("CREATE TABLE IF NOT EXISTS publisher(name text primary key not null, founded text)")

    def table_y(self):
        cur.execute("CREATE TABLE IF NOT EXISTS years(year text primary key not null)")

    def table_g(self):
        cur.execute("CREATE TABLE IF NOT EXISTS genres(genre text primary key not null)")

    def select(self, x):
        MainWindow.selector = x
        print("aaa")



class book(Screen):

    def new(self, x):
        x.append("no")
        try:
            cur.execute("INSERT INTO book VALUES (:name, :original, :publisher, :genre, :year)",
                        {"name": x[0], "original": x[1], "publisher": x[2], "genre": x[3], "year": x[4]})
            conn.commit()

            existor = []

            for i in cur.execute("select * from publisher"):
                if str(i[0]) == str(x[2]):
                    pass
                else:
                    existor.append(0)

            if len(existor) == len(list(cur.execute("select * from publisher"))):
                publisher.new(None, (str(x[2]), "69"))

            existor = []

            for i in cur.execute("select * from genres"):
                if str(i[0]) == str(x[3]):
                    pass
                else:
                    existor.append(0)

            if len(existor) == len(list(cur.execute("select * from genres"))):
                genre.new(None, (str(x[3])))

            existor = []

            for i in cur.execute("select * from years"):
                if str(i[0]) == str(x[4]):
                    pass
                else:
                    existor.append(0)

            if len(existor) == len(list(cur.execute("select * from years"))):
                years.new(None, (str(x[4])))


        except:
            print("no values")

    def butts(self):
        try:
            lis = cur.execute("SELECT * FROM book")
            l = []
            for i in lis:
                l.append(list(i))

            for i in l:
                z = Button(text=f'{str(i[0])} ({str(i[1])})', on_press=lambda x, j=i: MainWindow.select(None, j[0]))
                yield z
        except:
            pass

    def lily(self, x, y, z, a, b, c):
        y.text = ""
        z.text = ""
        a.text = ""
        b.text = ""
        c.text = ""
        return [x.add_widget(i) for i in self.butts()]

    def edit(self, x):
        cur.execute("update book set original = :original, publisher = :publisher, genre = :genre, year = :year where name = :name",
                    {"name": x[0], "original": x[1], "publisher": x[2], "genre": x[3], "year": x[4]})
        conn.commit()

    def deletion(self):
        try:
            cur.execute("delete from book where name = :name", {"name": MainWindow.selector})
            conn.commit()

        except:
            print('Red je već obrisan.')

    def err(self):
        print("something went to shit")


class publisher(Screen):

    def new(self, x):
        x.append("no")
        try:
            cur.execute("INSERT INTO publisher VALUES (:name, :founded)",
                        {"name": x[0], "founded": x[1]})
            conn.commit()

        except:
            print("no values")

    def butts(self):
        try:
            lis = cur.execute("SELECT * FROM publisher")
            l = []
            for i in lis:
                l.append(list(i))

                z = Button(text=str(i[0]), on_press=lambda x, j=i: MainWindow.select(None, j[0]))
                yield z
        except:
            pass

    def lily(self, x, y, z):
        y.text = ""
        z.text = ""
        return [x.add_widget(i) for i in self.butts()]

    def edit(self, x):
        cur.execute(
            "update publisher set founded = :founded where name = :name",
            {"name": x[0], "founded": x[1]})
        conn.commit()

    def deletion(self):
        try:
            cur.execute("delete from publisher where name = :name", {"name": MainWindow.selector})
            conn.commit()

        except:
            print('Red je već obrisan.')

    def err(self):
        print("something went to shit")


class years(Screen):

    def new(self, x):
        x.append("no")
        try:
            cur.execute("INSERT INTO years VALUES(:year)",
                        {"year": x[0]})
            conn.commit()

        except:
            print("no values")

    def butts(self):
        try:
            lis = cur.execute("SELECT * FROM years")
            l = []
            for i in lis:
                l.append(list(i))

            for i in l:
                z = Button(text=str(i[0]), on_press=lambda x, j=i: MainWindow.select(None, j[0]))
                yield z
        except:
            pass

    def lily(self, x, y):
        y.text = ""
        return [x.add_widget(i) for i in self.butts()]

    def deletion(self):
        try:
            cur.execute("delete from years where year = :year", {"year": MainWindow.selector})
            conn.commit()

        except:
            print('Red je već obrisan.')


class genre(Screen):

    def new(self, x):
        x.append("no")
        try:
            cur.execute("INSERT INTO genres VALUES(:genre)",
                        {"genre": x[0]})
            conn.commit()

        except:
            print("no values")

    def butts(self):
        try:
            lis = cur.execute("SELECT * FROM genres")
            l = []
            for i in lis:
                l.append(list(i))

            for i in l:
                z = Button(text=str(i[0]), on_press=lambda x, j=i: MainWindow.select(None, j[0]))
                yield z
        except:
            pass

    def lily(self, x, y):
        y.text = ""

        return [x.add_widget(i) for i in self.butts()]

    def deletion(self):
        try:
            cur.execute("delete from genres where genre = :genre", {"genre": MainWindow.selector})
            conn.commit()

        except:
            print('Red je već obrisan.')


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("project.kv")

class ProjectApp(App):
    def build(self):
        self.title = "LibreBase"
        return kv


if __name__ == '__main__':
    ProjectApp().run()
