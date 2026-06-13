import json
import os
import urllib.parse
import webbrowser


class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __str__(self):
        return f"Tytuł: {self.title} \nOpis: {self.content} \n"
    def to_dict(self):
        """Metoda do zmiany obiektu notatki na slownik, do zapisu JSON"""
        return {"title": self.title, "content": self.content}

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
                    self.notes.append(Note(item["title"],item["content"]))
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

    def send_mail(self, index, whereto):
        real_index = index - 1
        if real_index > len(self.notes):
            print(f"---Błąd. Nie ma notatki o takim numerze---\n")
            return

        title = self.notes[real_index].title
        content = self.notes[real_index].content

        m_title = f"Notatka: {title}"
        m_content = f"Przesyłam notatkę:\n\n {content}"

        # Konwersja na URL tak aby :mailto mogło ładnie obsłużyć całą wiadomość wraz ze znakami
        m_coded_title = urllib.parse.quote(m_title)
        m_coded_content = urllib.parse.quote(m_content)

        url = f"mailto:{whereto}?subject={m_coded_title}&body={m_coded_content}"

        # Wywołuje tutaj systemowy program poczty/
        webbrowser.open(url)
        print(f"Uruchomiono systemową pocztę dla adresata {whereto} z notatką o tytule {m_title}\n")

if __name__ == "__main__":
    notatnik = Notebook()
    notatnik.load_from_json()

    notatnik.add_note("Próba tytułu", "Próba zawartości")
    notatnik.add_note("Zakupy", "Kup piwo")
    notatnik.add_note("Nauka", "Naucz sie arabskiego")

    print("Sprawdzenie funkcji poczty")
    notatnik.send_mail(2,"jakisarabzpiwem@gmail.com")
