import DB
class Ucenik:
    def __init__(self, ID=None, ime='', prezime='', datumRodenja=''):
        self.ID = ID
        self.Ime = ime
        self.Prezime = prezime
        self.DatumRodenja = datumRodenja
        self.db = DB.DB()
        return
    
    def __repr__(self):
        return f'{self.Ime} {self.Prezime}'

    def __eq__(self, u):
        return self.ID == u.ID
    
    def __lt__(self, u):
        return self.Prezime < u.Prezime

    ##Metoda sprema podatke o učeniku u bazu, ako se radi
    ##o učeniku koji ima ID radi update inače radi insert
    def save(self):
        if self.ID != None: 
            upit = f'''UPDATE Ucenici SET
                    Ime = "{self.Ime}",
                    Prezime = "{self.Prezime}", 
                    DatumRodenja = "{self.DatumRodenja}" 
                    WHERE IDUcenika = "{self.ID}"'''
            self.db.updel(upit)
        else:
            upit = f'''INSERT INTO Ucenici (Ime, Prezime, DatumRodenja)
                        VALUES ("{self.Ime}",
                               "{self.Prezime}",
                               "{self.DatumRodenja}")'''
            self.ID = self.db.insert(upit)        
        
    ##Metoda briše učenika iz baze podataka
    def delete(self):
        upit = f'''DELETE FROM Ucenici WHERE IDUcenika = "{self.ID}"'''
        self.db.updel(upit)

    @staticmethod
    def all():
        upit = '''SELECT IDUcenika, Ime, Prezime, DatumRodenja 
                FROM Ucenici 
                ORDER BY Prezime ASC'''
        data = []
        for t in DB.DB().select(upit):
            u = Ucenik(int(t[0]), t[1], t[2], t[3])
            data.append(u)
        return data

class Nastavnik:
    def __init__(self, ID=None, ime='', prezime=''):
        self.ID = ID
        self.Ime = ime
        self.Prezime = prezime        
        self.db = DB.DB()
        return
    
    def __repr__(self):
        return f'{self.Ime} {self.Prezime}'

    def __eq__(self, u):
        return self.ID == u.ID
    
    def __lt__(self, u):
        return self.Prezime < u.Prezime
    
    def save(self):
        if self.ID != None: 
            upit = f'''UPDATE Nastavnici SET
                    Ime = "{self.Ime}",
                    Prezime = "{self.Prezime}" 
                    WHERE IDNastavnika = "{self.ID}"'''
            self.db.updel(upit)
        else:
            upit = f'''INSERT INTO Nastavnici (Ime, Prezime)
                        VALUES ("{self.Ime}",
                               "{self.Prezime}")'''
            self.ID = self.db.insert(upit)        
            
    def delete(self):
        upit = f'''DELETE FROM Nastavnici WHERE IDNastavnika = "{self.ID}"'''
        self.db.updel(upit)

    @staticmethod
    def all():
        upit = '''SELECT IDNastavnika, Ime, Prezime 
                FROM Nastavnici 
                ORDER BY Prezime ASC'''
        data = []
        for t in DB.DB().select(upit):
            u = Nastavnik(int(t[0]), t[1], t[2])
            data.append(u)
        return data

class SkolskaGodina:
    def __init__(self, ID=None, oznaka=''):
        self.ID = ID
        self.Oznaka = oznaka
        self.db = DB.DB()
        return
    
    def __repr__(self):
        return f'{self.Oznaka}'

    def __eq__(self, u):
        return self.ID == u.ID
    
    def __lt__(self, u):
        return self.Oznaka < u.Oznaka
    
    def save(self):
        if self.ID != None: 
            upit = f'''UPDATE SkolskeGodine SET
                    Oznaka = "{self.Oznaka}"                    
                    WHERE IDGodine = "{self.ID}"'''
            self.db.updel(upit)
        else:
            upit = f'''INSERT INTO SkolskeGodine (Oznaka)
                        VALUES ("{self.Oznaka}")'''
            self.ID = self.db.insert(upit)        
            
    def delete(self):
        upit = f'''DELETE FROM SkolskeGodine WHERE IDGodine = "{self.ID}"'''
        self.db.updel(upit)

    @staticmethod
    def all():
        upit = '''SELECT IDGodine, Oznaka
                FROM SkolskeGodine 
                ORDER BY Oznaka ASC'''
        data = []
        for t in DB.DB().select(upit):
            u = SkolskaGodina(int(t[0]), t[1])
            data.append(u)
        return data

    def razredi(self):
        temp = Razred.all()
        data = []
        for t in temp:
            if t.Godina == self:
                data.append(t)
        return data

class Razred:
    def __init__(self, ID=None, Odjeljenje='', Godina=None, Razrednik=None):
        self.ID = ID
        self.Odjeljenje = Odjeljenje
        ##Objekt tipa SkolskeGodine
        self.Godina = Godina
        ##Objekt tipa nastavnik
        self.Razrednik = Razrednik        
        self.db = DB.DB()
        return
        
    def __repr__(self):
        return f'{self. Odjeljenje} ({self.Razrednik.Ime} {self.Razrednik.Prezime})'

    def save(self):
        if self.ID != None:
            upit = f'''UPDATE Razredi SET Odjeljenje = "{self.Odjeljenje}", 
                      IDGodine = {self.Godina.ID},
                      IDNastavnika = {self.Razrednik.ID}
                      WHERE IDRazreda = {self.ID}'''
            self.db.updel(upit)
        else:
            upit = f'''INSERT INTO Razredi (Odjeljenje, IDGodine, IDNastavnika)
                      VALUES ("{self.Odjeljenje}", {self.Godina.ID},
                               {self.Razrednik.ID})'''
            self.ID = self.db.insert(upit)
        return
    
    def delete(self):
        upit = f'''DELETE FROM Razredi 
                   WHERE IDRazreda = {self.ID}'''
        self.db.updel(upit)
        return

    @staticmethod
    def all():
        upit = '''SELECT r.IDRazreda, r.Odjeljenje, n.IDNastavnika, n.Ime, n.Prezime, g.IDGodine, g.Oznaka
            FROM Razredi r
                LEFT JOIN Nastavnici n on n.IDNastavnika = r.IDNastavnika
                LEFT JOIN SkolskeGodine g on g.IDGodine = r.IDGodine
            ORDER BY r.Odjeljenje ASC'''
        data = []
        for t in DB.DB().select(upit):
            n = Nastavnik(t[2], t[3], t[4])
            g = SkolskaGodina(t[5], t[6])
            r = Razred(t[0], t[1], g, n)
            data.append(r)
        return data

    def ucenici(self):
        upit = f'''SELECT u.IDUcenika, u.Ime, u.Prezime, u.DatumRodenja
                FROM Ucenici u
                INNER JOIN UceniciRazredi ur ON ur.IDUcenika = u.IDUcenika
                WHERE ur.IDRazreda = {self.ID}
            ORDER BY u.Prezime ASC'''
        data = []
        for t in DB.DB().select(upit):
            u = Ucenik(t[0], t[1], t[2], t[3])            
            data.append(u)
        return data

    def dodaj_ucenika(self, u):
        upit = f'''SELECT * FROM UceniciRazredi
              WHERE IDUcenika = {u.ID} 
                   AND IDRazreda = {self.ID}'''
        a = self.db.select(upit)
        if len(a) == 0:
            upit = f'''INSERT INTO UceniciRazredi (IDUcenika, IDRazreda)
                 VALUES ({u.ID}, {self.ID})'''
            self.db.insert(upit)

    def obrisi_ucenika(self, u):
        upit = f'''DELETE FROM UceniciRazredi 
              WHERE IDUcenika = {u.ID} 
                    AND IDRazreda = {self.ID}'''
        self.db.updel(upit)


