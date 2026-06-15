import json
import os
import datetime
import urllib.parse
import webbrowser


class Note:
    def __init__(self, title, content, date=None, tags=None, modified_date=None):
        self.title = title
        self.content = content
        self.date = date or datetime.datetime.now()
        self.tags = tags if tags is not None else []
        self.modified_date = modified_date or date or datetime.datetime.now()

    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags else "Brak"
        return f"Tytuł: {self.title} \nOpis: {self.content} \nTagi: [{tags_str}] \nData utworzenia: {self.date.strftime('%Y-%m-%d %H:%M')}\n"
    def to_dict(self):
        """Metoda do zmiany obiektu notatki na slownik, do zapisu JSON"""
        return {"title": self.title, "content": self.content, "date": self.date.strftime('%Y-%m-%d %H:%M'), "tags": self.tags, "modified_date": self.modified_date.strftime('%Y-%m-%d %H:%M')}


class Notebook:
    def __init__(self, filename="notatki.json",tags_filename="tagi.json"):
        self.notes = []
        self.filename = filename
        self.tags_filename = tags_filename
        self.tags = {"Praca", "Szkoła", "Osobiste"}

    def add_note(self,title,content):
        notatka = Note(title,content)
        self.notes.append(notatka)
        print(f"Notatka dodana pomyślnie :) : '{title}' \n")

    # ======================
    # =============================
    # ZARZĄDZANIE GLOBALNYMI TAGAMI
    # =============================
    def add_new_tag_to_system(self, new_tag):
        """Dodaje nowy, unikalny tag do globalnej puli Notebooka"""
        formatted_tag = new_tag.strip()
        if not formatted_tag:  # Zabezpieczenie przed pustym tagiem
            print("--- Błąd: Tag nie może być pusty! ---\n")
            return

        existing_tags_lower = {tag.lower() for tag in self.tags}
        if formatted_tag.lower() in existing_tags_lower:
            print(f"--- Tag '{formatted_tag}' już istnieje w systemie! ---\n")
        else:
            self.tags.add(formatted_tag)  # Dodaje dokładnie tak, jak wpisał użytkownik
            print(f"--- Dodano nowy globalny tag: '{formatted_tag}' ---\n")

    def remove_tag_from_system(self, tag_name):
        """Usuwa tag z systemu (ignorując wielkość liter) i automatycznie odpina go ze wszystkich notatek"""
        search_tag = tag_name.strip().lower()

        # Szukamy oryginalnego tagu w bazie.
        exact_tag_to_remove = None
        for tag in self.tags:
            if tag.lower() == search_tag:
                exact_tag_to_remove = tag
                break

        if exact_tag_to_remove is None:
            print(f"--- Błąd: Tag '{tag_name.strip()}' nie istnieje w systemie ---\n")
            return

        # Usuwamy dokładną nazwę z globalnego zbioru
        self.tags.remove(exact_tag_to_remove)
        print(f"--- Globalny tag '{exact_tag_to_remove}' został usunięty z systemu. ---")

        # Usuwamy z notatek (List comprehension odfiltruje WSZYSTKIE wystąpienia tego tagu)
        cleared_count = 0
        for note in self.notes:
            # Sprawdzamy czy tag (wersja lowercase) był w tej notatce
            note_tags_lower = [t.lower() for t in note.tags]
            if search_tag in note_tags_lower:
                # Nadpisujemy listę tagów notatki, pomijając usuwany tag
                note.tags = [t for t in note.tags if t.lower() != search_tag]
                cleared_count += 1

        if cleared_count > 0:
            print(f"--- Automatycznie usunięto ten tag z {cleared_count} notatek. ---\n")
        else:
            print("--- Żadna notatka nie używała tego tagu. ---\n")

    def display_available_tags(self):
        """Wyświetla ponumerowaną listę globalnych tagów"""
        print("DODANE TAGI W SYSTEMIE:")
        for i, tag in enumerate(sorted(self.tags), start=1):
            print(f"{i}. {tag}")
        print()

    # =============================
    # ZARZĄDZANIE LOKALNYMI TAGAMI
    # =============================

    def add_tag_to_note(self, note_index, tag_name):
        """Przypisuje tag z globalnej puli do konkretnej notatki (case-insensitive)"""
        real_index = note_index - 1
        search_tag = tag_name.strip().lower()

        if not (0 <= real_index < len(self.notes)):
            print("--- Błąd. Nie ma notatki o takim numerze ---")
            return

        # Szukamy czy tag istnieje w systemie i pobieramy jego oryginalny zapis
        exact_system_tag = None
        for tag in self.tags:
            if tag.lower() == search_tag:
                exact_system_tag = tag
                break

        if exact_system_tag is None:
            print(f"--- Błąd: Tag '{tag_name.strip()}' nie istnieje w systemie. Dodaj go do notatnika! ---\n")
            return

        note = self.notes[real_index]
        # Sprawdzamy czy notatka już go nie ma
        if any(t.lower() == search_tag for t in note.tags):
            print(f"--- Notatka '{note.title}' ma już przypisany tag pasujący do '{tag_name.strip()}' ---\n")
        else:
            # Dodajemy oryginalną formę z systemu (np. "IT" zamiast "it")
            note.tags.append(exact_system_tag)
            print(f"--- Pomyślnie przypisano tag '{exact_system_tag}' do notatki '{note.title}' ---\n")

    def remove_tag_from_note(self, note_index, tag_name):
        """Usuwa wybrany tag tylko z jednej, konkretnej notatki (case-insensitive)"""
        real_index = note_index - 1
        search_tag = tag_name.strip().lower()

        if not (0 <= real_index < len(self.notes)):
            print("--- Błąd. Nie ma notatki o takim numerze ---")
            return

        note = self.notes[real_index]
        note_tags_lower = [t.lower() for t in note.tags]

        if search_tag in note_tags_lower:
            removed_tags = [t for t in note.tags if t.lower() == search_tag]
            note.tags = [t for t in note.tags if t.lower() != search_tag]
            print(f"--- Usunięto tag '{removed_tags[0]}' z notatki '{note.title}' ---\n")
        else:
            print(f"--- Ta notatka nie ma przypisanego tagu pasującego do '{tag_name.strip()}' ---\n")

    # ======================

    def save_to_json(self):
        notes_as_dict = [note.to_dict() for note in self.notes]
        try:
            with open(self.filename,"w",encoding="utf-8") as file:
                json.dump(notes_as_dict,file,ensure_ascii=False,indent=4)
                print("---Zapisano pliki do JSON.---")
        except Exception as e:
            print(f"Błąd podczas zapisu do JSON {e}")
        #zapis tagów
        try:
            with open(self.tags_filename, "w", encoding="utf-8") as file:
                json.dump(
                    list(sorted(self.tags)), file, ensure_ascii=False, indent=4
                )
                print("--- Zapisano globalne tagi do JSON. ---")
        except Exception as e:
            print(f"Błąd podczas zapisu tagów do JSON: {e}")

    def load_from_json(self):
        #część ładowania tagów
        if os.path.exists(self.tags_filename):
            try:
                with open(self.tags_filename, "r", encoding="utf-8") as file:
                    raw_tags = json.load(file)
                    self.tags = set(raw_tags)
                print(f"--- Wczytano globalne tagi z {self.tags_filename} ---")
            except Exception as e:
                print(f"--- Błąd podczas wczytywania tagów: {e} ---")
        else:
            print("--- Brak pliku tagów. Załadowano domyślne: Praca, Szkoła, Osobiste ---")
        #część ładowania notatek
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
                    modified_date = datetime.datetime.strptime(item.get("modified_date", item["date"]),
                                                               "%Y-%m-%d %H:%M")
                    note_tags = item.get("tags", [])
                    self.notes.append(Note(item["title"], item["content"], date, note_tags, modified_date))
                    self.tags.update(note_tags) # zabezpieczenie jakby cos sie stalo plikowi tagi.json
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

    def edit_note(self,index,new_title=None,new_content=None):
        real_index = index -1
        if 0 <= real_index < len(self.notes):
            updated = False
            if new_title is not None:
                self.notes[real_index].title = new_title
                updated = True
            if new_content is not None:
                self.notes[real_index].content = new_content
                updated = True
            if updated:
                self.notes[real_index].modified_date = datetime.datetime.now()
                print(f"---Zaktualizowano notatke nr {index}---\n")
            else:
                print("---Nic nie zmieniono (brak nowych wartości)---\n")
        else:
            print("--- Błąd. Nie ma notatki o takim numerze ---\n")

    def read_single_note(self, index):
        real_index = index - 1
        if 0 <= real_index < len(self.notes):
            print(f"--- Wyświetlam notatkę nr {index} ---")
            print(self.notes[real_index])
        else:
            print("---Błąd. Nie ma notatki o takim numerze---\n")

    def send_mail(self, index, whereto):
        real_index = index - 1
        if not (0 <= real_index < len(self.notes)):
            print(f"---Błąd. Nie ma notatki o takim numerze---\n")
            return

        title = self.notes[real_index].title
        content = self.notes[real_index].content

        m_title = f"Notatka: {title}"
        m_content = f"Przesyłam notatkę:\n\n {content}"

        # Kodowanie URI tak aby :mailto mogło ładnie obsłużyć całą wiadomość wraz ze znakami
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

    print("STAN PRZED ZMIANAMI:")
    notatnik.read_notes(5)

    notatnik.edit_note(2, new_title="Zakupy na weekend", new_content="Kup piwo i więcej piwa")
    notatnik.delete_notes(1)

    print("STAN PO ZMIANACH:")
    notatnik.read_notes(5)
    notatnik.save_to_json()
    notatnik.read_single_note(1)

    print("=== URUCHAMIANIE TESTÓW SYSTEMU TAGÓW ===\n")

    #Inicjalizacja notatnika i czyszczenie starych plików do testów (opcjonalnie)
    notatnik = Notebook("test_notatki.json", "test_tagi.json")
    notatnik.load_from_json()
    print("-" * 40)

    #Test dodawania notatek
    print("TEST 1: Dodawanie notatek...")
    notatnik.add_note("Projekt Python", "Napisac backend notatnika z Bolkiem")
    notatnik.add_note("Trening", "Zrobic klatke i biceps")
    print("-" * 40)

    #Test globalnych tagów
    print("TEST 2: Zarządzanie globalnymi tagami...")
    notatnik.display_available_tags()

    #Dodajemy nowy unikalny tag
    notatnik.add_new_tag_to_system("Siłownia")
    #Próba dodania duplikatu
    notatnik.add_new_tag_to_system("praca")
    notatnik.display_available_tags()
    print("-" * 40)

    #Test przypisywania tagów do notatek
    print("TEST 3: Przypisywanie tagów do notatek...")

    #Sytuacja poprawna
    notatnik.add_tag_to_note(1, "Praca")
    notatnik.add_tag_to_note(1, "Szkoła")
    notatnik.add_tag_to_note(2, "Siłownia")

    #Wymuszenie błędu: próba przypisania tagu, którego NIE MA w systemie
    print("Oczekiwany błąd poniżej (tag nie istnieje):")
    notatnik.add_tag_to_note(2, "Zdrowie")

    #Wymuszenie błędu: proba przypisania tego samego tagu drugi raz do tej samej notatki
    print("\nOczekiwany błąd poniżej (duplikat w notatce):")
    notatnik.add_tag_to_note(1, "Praca")
    print("-" * 40)

    #Wyświetlenie stanu przed zapisem
    print("TEST 4: Podgląd notatek z tagami przed zapisem...")
    notatnik.read_notes(2)
    print("-" * 40)

    #Test Zapisu do plików
    print("TEST 5: Zapis do osobnych plików JSON...")
    notatnik.save_to_json()
    print("-" * 40)

    #Test Odczytu
    print("TEST 6: Reset bazy danych w pamięci i odczyt z JSON...")
    nowy_notatnik = Notebook("test_notatki.json", "test_tagi.json")
    nowy_notatnik.load_from_json()

    print("\nNotatki załadowane z pliku (powinny mieć swoje tagi):")
    nowy_notatnik.read_notes(2)

    print("Globalne tagi załadowane z pliku (powinien być tam tag 'Siłownia'):")
    nowy_notatnik.display_available_tags()

    print("-" * 40)
    print("TEST 7: Testy usuwania tagów...")

    nowy_notatnik.remove_tag_from_note(1, "Szkoła")
    nowy_notatnik.remove_tag_from_system("Siłownia")

    print("Stan końcowy po usunięciu tagów:")
    nowy_notatnik.read_notes(2)
    nowy_notatnik.display_available_tags()

    print("=== KONIEC TESTÓW ===")
