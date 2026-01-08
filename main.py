import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
import sqlite3
import library
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

    def tableBook(self):
        cur.execute("CREATE TABLE IF NOT EXISTS book(name text primary key not null, original text not null, publisher text not null, genre text not null, year text not null)")

    def tablePublisher(self):
        cur.execute("CREATE TABLE IF NOT EXISTS publisher(name text primary key not null, founded text)")

    def tableYear(self):
        cur.execute("CREATE TABLE IF NOT EXISTS years(year text primary key not null)")

    def tableGenre(self):
        cur.execute("CREATE TABLE IF NOT EXISTS genres(genre text primary key not null)")

    def select(self, item):
        MainWindow.selector = item


class book(Screen):
    def new(self, values):
        try:
            cur.execute("INSERT INTO book VALUES (:name, :original, :publisher, :genre, :year)",
                        {"name": values[0], "original": values[1], "publisher": values[2], "genre": values[3], "year": values[4]})
            conn.commit()

            existor = []
            check = False

            for i in cur.execute("select * from publisher"):
                if not check:
                    if str(i[0]) == str(values[2]):
                        pass
                    else:
                        existor.append(values[2])
                        check = True

            if check:
                publisher.new(None, (str(values[2]), "69"))

            existor = []
            check = False

            for i in cur.execute("select * from genres"):
                if not check:
                    if str(i[0]) == str(values[3]):
                        pass
                    else:
                        existor.append(values[3])
                        check = True

            if check:
                genre.new(None, (str(values[3])))

            existor = []
            check = False

            for i in cur.execute("select * from years"):
                if not check:
                    if str(i[0]) == str(values[4]):
                        pass
                    else:
                        existor.append(values[4])
                        check = True

            if check:
                years.new(None, (str(values[4])))

        except:
            print("no values")

    def buttons(self):
        try:
            results = cur.execute("SELECT * FROM book")
            itemList = []
            for i in results:
                itemList.append(list(i))

            for i in itemList:
                button = Button(text=f'{str(i[0])} ({str(i[1])})', on_press=lambda x, j=i: MainWindow.select(None, j[0]))
                yield button
        except:
            pass

    def createListView(self, listView, name, originalName, publisher, genre, year):
        name.text = ""
        originalName.text = ""
        publisher.text = ""
        genre.text = ""
        year.text = ""
        return [listView.add_widget(i) for i in self.buttons()]

    def edit(self, values):
        cur.execute("update book set original = :original, publisher = :publisher, genre = :genre, year = :year where name = :name",
                    {"name": values[0], "original": values[1], "publisher": values[2], "genre": values[3], "year": values[4]})
        conn.commit()

    def deletion(self):
        try:
            cur.execute("delete from book where name = :name", {"name": MainWindow.selector})
            conn.commit()

        except:
            print('Red je već obrisan.')

    def error(self):
        print("something went wrong")


class publisher(Screen):
    def new(self, values):
        try:
            cur.execute("INSERT INTO publisher VALUES (:name, :founded)",
                        {"name": values[0], "founded": values[1]})
            conn.commit()

            existor = []
            check = False

            for i in cur.execute("select * from years"):
                if not check:
                    if str(i[0]) == str(values[1]):
                        pass
                    else:
                        existor.append(values[1])
                        check = True

            if check:
                years.new(None, (str(values[1])))
        except:
            print("no values")

    def buttons(self):
        try:
            items = cur.execute("SELECT * FROM publisher")
            listView = []
            for i in items:
                listView.append(list(i))

                button = Button(text=str(i[0]), on_press=lambda x, j=i: MainWindow.select(None, j[0]))
                yield button
        except:
            pass

    def createListView(self, scrollView, name, year):
        name.text = ""
        year.text = ""
        return [scrollView.add_widget(i) for i in self.buttons()]

    def edit(self, values):
        cur.execute(
            "update publisher set founded = :founded where name = :name",
            {"name": values[0], "founded": values[1]})
        conn.commit()

    def deletion(self):
        try:
            cur.execute("delete from publisher where name = :name", {"name": MainWindow.selector})
            conn.commit()

        except:
            print('Red je već obrisan.')

    def error(self):
        print("something went to shit")


class years(Screen):
    def new(self, values):
        try:
            cur.execute("INSERT INTO years VALUES(:year)",
                        {"year": values[0]})
            conn.commit()

        except:
            print("no values")

    def buttons(self):
        try:
            items = cur.execute("SELECT * FROM years")
            listView = []
            for i in items:
                listView.append(list(i))

            for i in listView:
                button = Button(text=str(i[0]), on_press=lambda x, j=i: MainWindow.select(None, j[0]))
                yield button
        except:
            pass

    def createListView(self, scrollView, years):
        years.text = ""
        return [scrollView.add_widget(i) for i in self.buttons()]

    def deletion(self):
        try:
            cur.execute("delete from years where year = :year", {"year": MainWindow.selector})
            conn.commit()

        except:
            print('Red je već obrisan.')


class genre(Screen):
    def new(self, value):
        try:
            cur.execute("INSERT INTO genres VALUES(:genre)",
                        {"genre": value[0]})
            conn.commit()

        except:
            print("no values")

    def buttons(self):
        try:
            items = cur.execute("SELECT * FROM genres")
            listView = []
            for i in items:
                listView.append(list(i))

            for i in listView:
                button = Button(text=str(i[0]), on_press=lambda x, j=i: MainWindow.select(None, j[0]))
                yield button
        except:
            pass

    def createListView(self, scrollView, items):
        items.text = ""

        return [scrollView.add_widget(i) for i in self.buttons()]

    def deletion(self):
        try:
            cur.execute("delete from genres where genre = :genre", {"genre": MainWindow.selector})
            conn.commit()

        except:
            print('Red je već obrisan.')


class browseBook(Screen):
    def buttons(self):
        try:
            items = cur.execute("SELECT * FROM book")
            listView = []
            for i in items:
                listView.append(list(i))

            for i in listView:
                button = Button(text=str(i[0]), on_press=lambda x, j=i: MainWindow.select(None, j[0]))
                yield button
        except:
            pass

    def createListView(self, scrollView):
        if library.provjera("book"):
            return [scrollView.add_widget(i) for i in self.buttons()]
        else:
            return [scrollView.add_widget(Button(text=str("Tablica je prazna")))]


class browsePublisher(Screen):
    def buttons(self):
        try:
            items = cur.execute("SELECT * FROM publisher")
            listView = []
            for i in items:
                listView.append(list(i))

            for i in listView:
                button = Button(text=str(i[0]), on_press=lambda x, j=i: MainWindow.select(None, j[0]))
                yield button
        except:
            pass

    def createListView(self, scrollView):
        if library.provjera("publisher"):

            return [scrollView.add_widget(i) for i in self.buttons()]
        else:
            return [scrollView.add_widget(Button(text=str("Tablica je prazna")))]


class browseYear(Screen):
    def buttons(self):
        try:
            items = cur.execute("SELECT * FROM years")
            listView = []
            for i in items:
                listView.append(list(i))

            for i in listView:
                button = Button(text=str(i[0]), on_press=lambda x, j=i: MainWindow.select(None, j[0]))
                yield button
        except:
            pass

    def createListView(self, scrollView):
        if library.provjera("years"):

            return [scrollView.add_widget(i) for i in self.buttons()]
        else:
            return [scrollView.add_widget(Button(text=str("Tablica je prazna")))]


class browseGenre(Screen):
    def buttons(self):
        try:
            items = cur.execute("SELECT * FROM genres")
            listView = []
            for i in items:
                listView.append(list(i))

            for i in listView:
                button = Button(text=str(i[0]), on_press=lambda x, j=i: MainWindow.select(None, j[0]))
                yield button
        except:
            pass

    def createListView(self, scrollView):
        if library.provjera("genres"):

            return [scrollView.add_widget(i) for i in self.buttons()]
        else:
            return [scrollView.add_widget(Button(text=str("Tablica je prazna")))]

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("project.kv")


class ProjectApp(App):
    def build(self):
        self.title = "LibreBase"
        return kv


if __name__ == '__main__':
    ProjectApp().run()
