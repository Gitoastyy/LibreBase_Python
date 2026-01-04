from sqlite3 import *
class DB:
    def __init__(self, baza='skola.db'):
        self.B = baza
        
    def select(self, upit):
        conn = connect(self.B)
        cur = conn.cursor()
        data = []
        for t in cur.execute(upit):
            data.append(t)
        conn.close()
        return data
        
    def insert(self, upit):
        conn = connect(self.B)
        cur = conn.cursor()
        cur.execute(upit)
        n = cur.lastrowid
        conn.commit()
        conn.close()
        return n
        
    def updel(self, upit):
        conn = connect(self.B)
        cur = conn.cursor()
        cur.execute(upit)       
        conn.commit()
        conn.close()

    def kreirajBazu(self):
        upit = '''CREATE TABLE Ucenici (
           IDUcenika INTEGER PRIMARY KEY AUTOINCREMENT,
           Ime TEXT NOT NULL, 
           Prezime TEXT NOT NULL, 
           DatumRodenja TEXT,
           EMailAdresa TEXT
           )'''
        self.updel(upit)

        upit = '''CREATE TABLE Nastavnici (
           IDNastavnika INTEGER PRIMARY KEY AUTOINCREMENT,
           Ime TEXT NOT NULL, 
           Prezime TEXT NOT NULL)'''
        self.updel(upit)

        upit = '''CREATE TABLE SkolskeGodine (
           IDGodine INTEGER PRIMARY KEY AUTOINCREMENT,
           Oznaka TEXT NOT NULL)'''
        self.updel(upit)
        
        upit =  '''CREATE TABLE Razredi (IDRazreda INTEGER PRIMARY KEY AUTOINCREMENT,
           Odjeljenje TEXT NOT NULL,
           IDNastavnika INTEGER REFERENCES Nastavnici(IDNastavnika), 
           IDGodine INTEGER REFERENCES SkolskeGodine(IDGodine))'''
        self.updel(upit)

        
        upit =  '''CREATE TABLE UceniciRazredi (
           IDRazreda INTEGER REFERENCES Razredi(IDRazreda),            
           IDUcenika INTEGER REFERENCES Ucenici(IDUcenika))'''
        self.updel(upit)

        print('Baza je kreirana')
