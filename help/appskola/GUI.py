from tkinter import *
from tkinter.messagebox import *
from Model import *
class UcenikSucelje(Toplevel):
    def __init__(self, root):
        self.R = root        
        super().__init__(self.R)
        self.title('Učenici')        
        self.grid()
        self.kreirajSucelje()        
        return
    
    def kreirajSucelje(self):
        self.Popis = Listbox(self, exportselection=0)
        self.Popis.grid(row=0, column=0, rowspan=4)
        Label(self, text='Ime').grid(row=0, column=1, sticky='W')
        self.Ime = StringVar()
        Entry(self, textvariable=self.Ime).grid(row=0, column=2, columnspan=2)
        Label(self, text='Prezime').grid(row=1, column=1, sticky='W')
        self.Prezime = StringVar()
        Entry(self, textvariable=self.Prezime).grid(row=1, column=2, columnspan=2)
        Label(self, text='Datum rođenja').grid(row=2, column=1, sticky='W')
        self.DR = StringVar()
        Entry(self, textvariable=self.DR).grid(row=2, column=2, columnspan=2)       
        Button(self, text='Novi', command=self.novi).grid(row=3, column=1)
        Button(self, text='Spremi', command=self.spremi).grid(row=3, column=2)
        Button(self, text='Obriši', command=self.obrisi).grid(row=3, column=3)
        ##Učitavanje podataka o učenicima u Listbox
        self.Ucenici = Ucenik.all()
        for u in self.Ucenici:
            self.Popis.insert(END, u)
        self.Popis.bind('<<ListboxSelect>>', self.ucitaj_ucenika)
        return
        
    def novi(self):
        self.Popis.selection_clear(0, END)
        self.Ime.set('')
        self.Prezime.set('')
        self.DR.set('')

        
    def spremi(self):
        # Provjeravamo je li odabrana neka stavka liste s popisom
        if len(self.Popis.curselection()) == 0:
            # Primijetimo da moramo uključiti modul Model 
            u = Ucenik()
            # Primijetimo da moramo uključiti modul tkinter.messagebox
            poruka = 'Učenik je dodan'
        else:
            n = int(self.Popis.curselection()[0])
            u = self.Ucenici[n]
            poruka = 'Podatci o učeniku su promijenjeni'
        u.Ime = self.Ime.get()
        u.Prezime = self.Prezime.get()
        u.DatumRodenja = self.DR.get()
        u.save()
        self.Popis.delete(0, END)
        self.Ucenici = Ucenik.all()
        for i in range(len(self.Ucenici)):
            self.Popis.insert(END, self.Ucenici[i])
            if self.Ucenici[i].ID == u.ID:
                self.Popis.selection_set(i)        
        showinfo('Učenici', poruka)
        
    def obrisi(self):
        if len(self.Popis.curselection()) == 0:
            showerror('Učenici', 'Niste odabrali učenika')
        else:
            if askyesno('Učenici', 'Jeste li sigurni da želite obrisati učenika?'):
                n = int(self.Popis.curselection()[0])
                u = self.Ucenici[n]
                self.Ucenici.pop(n)
                self.Popis.delete(n)    
                u.delete()   
                self.novi()


    def ucitaj_ucenika(self, e=None):
        ##Dohvaćamo odabranu stavku unutar liste
        n = int(self.Popis.curselection()[0])
        ##Pripadnog učenika (objekt) stavljamo u varijablu u
        u = self.Ucenici[n]
        self.Ime.set(u.Ime)
        self.Prezime.set(u.Prezime)
        self.DR.set(u.DatumRodenja)        

class NastavnikSucelje(Toplevel):
    def __init__(self, root):
        self.R = root        
        super().__init__(self.R)
        self.title('Nastavnici')        
        self.grid()
        self.kreirajSucelje()        
        return
    
    def kreirajSucelje(self):
        self.Popis = Listbox(self, exportselection=0)
        self.Popis.grid(row=0, column=0, rowspan=3)
        Label(self, text='Ime').grid(row=0, column=1, sticky='W')
        self.Ime = StringVar()
        Entry(self, textvariable=self.Ime).grid(row=0, column=2, columnspan=2)
        Label(self, text='Prezime').grid(row=1, column=1, sticky='W')
        self.Prezime = StringVar()
        Entry(self, textvariable=self.Prezime).grid(row=1, column=2, columnspan=2)            
        Button(self, text='Novi', command=self.novi).grid(row=3, column=1)
        Button(self, text='Spremi', command=self.spremi).grid(row=3, column=2)
        Button(self, text='Obriši', command=self.obrisi).grid(row=3, column=3)       
        self.Nastavnici = Nastavnik.all()
        for n in self.Nastavnici:
            self.Popis.insert(END, n)
        self.Popis.bind('<<ListboxSelect>>', self.ucitaj_nastavnika)
        return
        
    def novi(self):
        self.Popis.selection_clear(0, END)
        self.Ime.set('')
        self.Prezime.set('')       

        
    def spremi(self):        
        if len(self.Popis.curselection()) == 0:            
            na = Nastavnik()           
            poruka = 'Nastavnik je dodan'
        else:
            n = int(self.Popis.curselection()[0])
            na = self.Nastavnici[n]
            poruka = 'Podatci o nastavniku su promijenjeni'
        na.Ime = self.Ime.get()
        na.Prezime = self.Prezime.get()        
        na.save()
        self.Popis.delete(0, END)
        self.Nastavnici = Nastavnik.all()
        for i in range(len(self.Nastavnici)):
            self.Popis.insert(END, self.Nastavnici[i])
            if self.Nastavnici[i].ID == na.ID:
                self.Popis.selection_set(i)        
        showinfo('Nastavnici', poruka)
        
    def obrisi(self):
        if len(self.Popis.curselection()) == 0:
            showerror('Nastavnici', 'Niste odabrali nastavnika')
        else:
            if askyesno('Nastavnici', 'Jeste li sigurni da želite obrisati nastavnika?'):
                n = int(self.Popis.curselection()[0])
                na = self.Nastavnici[n]
                self.Nastavnici.pop(n)
                self.Popis.delete(n)    
                na.delete()   
                self.novi()


    def ucitaj_nastavnika(self, e=None):        
        n = int(self.Popis.curselection()[0])        
        na = self.Nastavnici[n]
        self.Ime.set(na.Ime)
        self.Prezime.set(na.Prezime)


class SkolskaGodinaSucelje(Toplevel):
    def __init__(self, root):
        self.R = root        
        super().__init__(self.R)
        self.title('Školske godine')        
        self.grid()
        self.kreirajSucelje()        
        return
    
    def kreirajSucelje(self):
        self.Popis = Listbox(self, exportselection=0)
        self.Popis.grid(row=0, column=0, rowspan=2)
        Label(self, text='Oznaka').grid(row=0, column=1, sticky='W')
        self.Oznaka = StringVar()
        Entry(self, textvariable=self.Oznaka).grid(row=0, column=2, columnspan=2)                
        Button(self, text='Novi', command=self.novi).grid(row=3, column=1)
        Button(self, text='Spremi', command=self.spremi).grid(row=3, column=2)
        Button(self, text='Obriši', command=self.obrisi).grid(row=3, column=3)       
        self.Godine = SkolskaGodina.all()
        for g in self.Godine:
            self.Popis.insert(END, g)
        self.Popis.bind('<<ListboxSelect>>', self.ucitaj_godinu)
        return
        
    def novi(self):
        self.Popis.selection_clear(0, END)
        self.Oznaka.set('')            
        
    def spremi(self):        
        if len(self.Popis.curselection()) == 0:            
            g = SkolskaGodina()           
            poruka = 'Školska godina je dodana'
        else:
            n = int(self.Popis.curselection()[0])
            g = self.Godine[n]
            poruka = 'Podatci o školskog godini su promijenjeni'
        g.Oznaka = self.Oznaka.get()            
        g.save()
        self.Popis.delete(0, END)
        self.Godine = SkolskaGodina.all()
        for i in range(len(self.Godine)):
            self.Popis.insert(END, self.Godine[i])
            if self.Godine[i].ID == g.ID:
                self.Popis.selection_set(i)        
        showinfo('Školske godine', poruka)
        
    def obrisi(self):
        if len(self.Popis.curselection()) == 0:
            showerror('Školske godine', 'Niste odabrali školsku godinu')
        else:
            if askyesno('Školske godine', 'Jeste li sigurni da želite obrisati školsku godinu?'):
                n = int(self.Popis.curselection()[0])
                g = self.Godine[n]
                self.Godine.pop(n)
                self.Popis.delete(n)    
                g.delete()   
                self.novi()


    def ucitaj_godinu(self, e=None):        
        n = int(self.Popis.curselection()[0])        
        g = self.Godine[n]
        self.Oznaka.set(g.Oznaka)        

class RazredSucelje(Toplevel):
    def __init__(self, root):
        self.R = root        
        super().__init__(self.R)
        self.title('Razredi')            
        self.grid()
        self.kreirajSucelje()        
        return
    
    def kreirajSucelje(self):
        self.Popis = Listbox(self, exportselection=0)
        self.Popis.grid(row=0, column=0, rowspan=4)
        Label(self, text='Odjeljenje').grid(row=0, column=1, sticky='W')
        self.Odjeljenje = StringVar()
        Entry(self, textvariable=self.Odjeljenje).grid(row=0, column=2, columnspan=2)
        
        Label(self, text='Školska godina').grid(row=1, column=1, sticky='W')
        self.SkolskaGodina = StringVar()
        self.Godine = SkolskaGodina.all()
        self.SGPopis = OptionMenu(self, self.SkolskaGodina, *self.Godine)
        self.SGPopis.grid(row=1, column=2)

        Label(self, text='Razrednik').grid(row=2, column=1, sticky='W')
        self.Razrednik = StringVar()
        self.Nastavnici = Nastavnik.all()
        self.NPopis = OptionMenu(self, self.Razrednik, *self.Nastavnici)
        self.NPopis.grid(row=2, column=2)
        
        Button(self, text='Novi', command=self.novi).grid(row=3, column=1)
        Button(self, text='Spremi', command=self.spremi).grid(row=3, column=2)
        Button(self, text='Obriši', command=self.obrisi).grid(row=3, column=3)
        self.Razredi = Razred.all()
        
        
        for r in self.Razredi:
            self.Popis.insert(END, r.Odjeljenje)
        self.Popis.bind('<<ListboxSelect>>', self.ucitaj_razred)
        return
        
    def novi(self):
        self.Popis.selection_clear(0, END)
        self.Odjeljenje.set('')
        self.SkolskaGodina.set('')
        self.Razrednik.set('')
        
    def spremi(self):        
        if len(self.Popis.curselection()) == 0:            
            r = Razred()           
            poruka = 'Razred je dodan'
        else:
            n = int(self.Popis.curselection()[0])
            r = self.Razredi[n]
            poruka = 'Podatci o razredui su promijenjeni'
        r.Odjeljenje = self.Odjeljenje.get()
        na = self.Razrednik.get()
        rt = None
        for t in self.Nastavnici:
            if na == str(t):
                rt = t
        
        g = self.SkolskaGodina.get()
        gt = None
        for t in self.Godine:
            if g == str(t):
                gt = t
                
        OK = True
        if rt is None:
            showError('Razredi', 'Niste odabrali razrednika')
            OK = False
        if gt is None:
            showError('Razredi', 'Niste odabrali školsku godinu')
            OK = False

        if OK:
            r.Razrednik = rt
            r.Godina = gt        
            r.save()
            self.Popis.delete(0, END)
            self.Razredi = Razred.all()
            for i in range(len(self.Razredi)):
                self.Popis.insert(END, self.Razredi[i].Odjeljenje)
                if self.Razredi[i].ID == r.ID:
                    self.Popis.selection_set(i)        
            showinfo('Razredi', poruka)
        
    def obrisi(self):
        if len(self.Popis.curselection()) == 0:
            showerror('Školske godine', 'Niste odabrali školsku godinu')
        else:
            if askyesno('Školske godine', 'Jeste li sigurni da želite obrisati školsku godinu?'):
                n = int(self.Popis.curselection()[0])
                r = self.Razredi[n]
                self.Razredi.pop(n)
                self.Popis.delete(n)    
                r.delete()   
                self.novi()


    def ucitaj_razred(self, e=None):        
        n = int(self.Popis.curselection()[0])        
        r = self.Razredi[n]
        self.Odjeljenje.set(r.Odjeljenje)
        self.SkolskaGodina.set(r.Godina)
        self.Razrednik.set(r.Razrednik)

class UcenikRazredSucelje(Toplevel):
    def __init__(self, root):
        self.R = root
        super().__init__(self.R)
        self.Title = 'Učenici po razredima'
        self.title(self.Title)
        self.grid()        
        self.kreirajSucelje()        

    def kreirajSucelje(self):
        h = 10
        self.L_sg = Listbox(self, height=h, exportselection=0)
        self.L_sg.grid(row=0, column=0)
        self.L_r = Listbox(self, height=h, exportselection=0)
        self.L_r.grid(row=1, column=0)
        self.L_u_r = Listbox(self, height=2*h, exportselection=0)
        self.L_u_r.grid(row=0, column=1, rowspan=2)
        Button(self, text='<', command=self.dodaj_u_razred).grid(row=0, column=2)
        Button(self, text='>', command=self.brisi_iz_razreda).grid(row=1, column=2)
        self.L_u_s = Listbox(self, height=2*h, exportselection=0)
        self.L_u_s.grid(row=0, column=3, rowspan=2)
        self.SG = []
        self.R = []
        self.U = []
        self.UR = []
        for t in SkolskaGodina.all():
            self.SG.append(t)
            self.L_sg.insert(END, t)
        for u in Ucenik.all():
            self.U.append(u)
            self.L_u_s.insert(END, u)
        self.L_sg.bind('<<ListboxSelect>>', self.ucitaj_razrede)
        self.L_r.bind('<<ListboxSelect>>', self.ucitaj_ucenike)
        
    def ucitaj_razrede(self, e=None):
        n = int(self.L_sg.curselection()[0])
        ##Učitavanje razreda za zadanu godinu čuvamo ih u listi      
        self.R = self.SG[n].razredi()
        self.L_r.delete(0, END)
        for r in self.R:
            self.L_r.insert(END, r)

    def ucitaj_ucenike(self, e=None):
        n = int(self.L_r.curselection()[0])
        self.L_u_r.delete(0, END)
        self.UR = []
        for u in self.R[n].ucenici():
            self.UR.append(u)
            self.L_u_r.insert(END, u) 

    def dodaj_u_razred(self):
        ##Provjera je li odabran razred
        if (len(self.L_r.curselection()) == 0):
            showerror(self.Title, 'Niste odabrali razred')
            return
        ##Provjera je li odabran učenik
        if (len(self.L_u_s.curselection()) == 0):
            showerror(self.Title, 'Niste odabrali učenika')
            return
        n = int(self.L_u_s.curselection()[0])
        m = int(self.L_r.curselection()[0])
        ##Provjera je li učenik već u razredu
        if self.U[n] in self.R[m].ucenici():  					#1
            showerror(self.Title, 'Učenik se već nalazi u razredu')
        else:
            ##Dodavanje učenika u razred na razini baze
            self.R[m].dodaj_ucenika(self.U[n])
            ##Dodavanje unutar sučelja            	    
            self.L_u_r.delete(0, END)
            self.UR = []
            for u in self.R[m].ucenici():
                self.UR.append(u)
                self.L_u_r.insert(END, u)

    def brisi_iz_razreda(self):   
        if (len(self.L_u_r.curselection()) == 0):
            showerror(self.Title, 'Niste odabrali učenika')
            return
        n = int(self.L_u_r.curselection()[0])
        m = int(self.L_r.curselection()[0])        
        self.R[m].obrisi_ucenika(self.UR[n])            
        self.L_u_r.delete(n)                



class GlavniProzor(Frame):
    def __init__(self, root):
        self.R = root
        self.R.title('Škola')
        super().__init__(self.R)
        self.kreirajSucelje()
        
    def kreirajSucelje(self):
        f = ('Segoe UI', 20, 'normal')
        s = 20
        Button(self, text='Učenici', font=f, width=s, command=self.ucenici).pack()
        Button(self, text='Nastavnici', font=f, width=s, command=self.nastavnici).pack()
        Button(self, text='Školske godine', font=f, width=s, command=self.skolske_godine).pack()
        Button(self, text='Razredi', font=f, width=s, command=self.razredi).pack()
        Button(self, text='Učenici po razredima', font=f, width=s, command=self.ucenici_razredi).pack()
        Button(self, text='Kraj', font=f, width=s, command=self.kraj).pack()
        self.pack()

    def ucenici(self):
        us = UcenikSucelje(self)

    def nastavnici(self):
        ns = NastavnikSucelje(self)

    def skolske_godine(self):
        sgs = SkolskaGodinaSucelje(self)

    def razredi(self):
        rs = RazredSucelje(self)

    def ucenici_razredi(self):
        urs = UcenikRazredSucelje(self)

    def kraj(self):
        if askyesno('Škola', 'Jeste li sigurni da želite napustiti aplikaciju?'):
            self.R.destroy()
        
if __name__ == '__main__':
    us = GlavniProzor(Tk())
    mainloop()
