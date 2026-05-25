import json
import os
import datetime


class Note:
    def __init__(self, title, content, date = None):
        self.title = title
        self.content = content
        self.date = date or datetime.datetime.now() #@KrzyzakPatryk, sprawdz to Jas. Generalnie @Pawel zasugerowal takie rozwiazanie, 
                                                    #sprawdza czy date jest pustym obiektem i jak tak to wchodzi systemowa data 
                                                    #a jak nie to to co wpisał użytkownik

    def __str__(self):
        return f"Tytuł: {self.title} \nOpis: {self.content} \nData utworzenia: {(self.date).strftime("%Y-%m-%d %H:%M")}\n"
    def to_dict(self):
        """Metoda do zmiany obiektu notatki na slownik, do zapisu JSON"""
        return {"title": self.title, "content": self.content, "date": (self.date).strftime("%Y-%m-%d %H:%M")}


class Notebook:
    def __init__(self,filename = "notatki.json"):
        self.notes = []
        self.filename = filename

    def add_note(self,title,content):
        notatka = Note(title,content)
        self.notes.append(notatka)
        print(f"Notatka dodana pomyślnie :) : '{title}' \n")

    def save_to_json(self):
        notes_as_dict = [note.to_dict() for note in self.notes]
        try:
            with open(self.filename,"w",encoding="utf-8") as file:
                json.dump(notes_as_dict,file,ensure_ascii=False,indent=4)
                print("---Zapisano pliki do JSON.---")
        except Exception as e:
            print(f"Błąd podczas zapisu do JSON {e}")

    def load_from_json(self):
        if not os.path.exists(self.filename):
            print("---Brak pliku JSON. Rozpoczęcie z pustym notatnikiem---")
            return
        try:
            with open(self.filename,"r",encoding="utf-8") as file:
                raw_data = json.load(file)
                self.notes = []
                for item in raw_data:
                    date = datetime.datetime.strptime(item["date"], "%Y-%m-%d %H:%M") #konwertuje tekst daty na obiekt daty 
                                                                                      #tak aby ładnie dało się na nim wykonywać operacje
                    self.notes.append(Note(item["title"], item["content"], date))
            print(f"---Wczytano {len(self.notes)} notatek z JSON.---")
        except Exception as e:
            print(f"---Błąd podczas wczytywania {e}---")

    def read_notes(self,n):
        if not self.notes:
            print ("Brak notatek do wyświetlenia. \n")
            return
        limit = min(n,len(self.notes))
        print(f"Wyświetlam {limit} notatek z {len(self.notes)} notatek. \n")
        for i in range (limit):
            print(f"{i+1}. {self.notes[i]}")

    def delete_notes(self,index):
        real_index = index -1
        if 0 <= real_index < len(self.notes):
            deleted_note = self.notes.pop(real_index)
            print(f"---Usunięto notatkę {deleted_note.title}---\n")
        else:
            print("---Błąd. Nie ma notatki o takim numerze---\n")

    def edit_notes(self,index,new_title=None,new_content=None):
        real_index = index -1
        if 0 <= real_index < len(self.notes):
            if new_title:
                self.notes[real_index].title = new_title
            if new_content:
                self.notes[real_index].content = new_content
            print(f"---Zaktualizowano notatke nr {index}---\n")
        else:
            print("---Błąd. Nie ma notatki o takim numerze---\n")

    def read_single_note(self, index):
        real_index = index - 1
        if 0 <= real_index < len(self.notes):
            print(f"--- Wyświetlam notatkę nr {index} ---")
            print(self.notes[real_index])
        else:
            print("---Błąd. Nie ma notatki o takim numerze---\n")

if __name__ == "__main__":
    notatnik = Notebook()
    notatnik.load_from_json()

    notatnik.add_note("Próba tytułu", "Próba zawartości")
    notatnik.add_note("Zakupy", "Kup piwo")
    notatnik.add_note("Nauka", "Naucz sie arabskiego")

    print("STAN PRZED ZMIANAMI:")
    notatnik.read_notes(5)

    notatnik.edit_notes(2, new_title="Zakupy na weekend", new_content="Kup piwo i więcej piwa")
    notatnik.delete_notes(1)

    print("STAN PO ZMIANACH:")
    notatnik.read_notes(5)
    notatnik.save_to_json()
    notatnik.read_single_note(1)
