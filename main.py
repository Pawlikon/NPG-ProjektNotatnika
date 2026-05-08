
class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __str__(self):
        return f"Tytuł: {self.title} \nOpis: {self.content} \n"

class Notebook:
    def __init__(self):
        self.notes = []
    def add_note(self,title,content):
        notatka = Note(title,content)
        self.notes.append(notatka)
        print(f"Notatka dodana pomyślnie :) : '{title}' \n")

    def read_notes(self,n):
        if not self.notes:
            print ("Brak notatek do wyświetlenia. \n")
            return
        limit = min(n,len(self.notes))
        print(f"Wyświetlam {limit} notatek z {len(self.notes)} notatek. \n")
        for i in range (limit):
            print(f"{i+1}. {self.notes[i]}")

if __name__ == "__main__":
    notatka = Notebook()
    notatka.add_note("Próba tytułu", "Próba zawartościiiiiiiiiiii")
    notatka.add_note("Zakupy", "Kup piwo")
    notatka.add_note("Nauka", "Naucz sie arabskiego")
    notatka.read_notes(2)
    notatka.read_notes(3)
