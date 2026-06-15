import streamlit as st
import datetime
from classes import Notebook, Note

st.set_page_config(page_title="Python Notes", page_icon="📝", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stApp { background-color: #f9f9fb; }
    .css-1d391kg { background-color: #f0f0f4; } /* Sidebar background */
    h1 { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE BACKEND IN SESSION STATE ---
if "notebook" not in st.session_state:
    st.session_state.notebook = Notebook("notatki.json", "tagi.json")
    st.session_state.notebook.load_from_json()

if "selected_note_index" not in st.session_state:
    st.session_state.selected_note_index = None

nb = st.session_state.notebook

with st.sidebar:
    st.title("Notatnik")

    # add new note    
    if st.button("Nowa notatka", use_container_width=True):
        nb.add_note("Bez tytułu", "")
        nb.save_to_json()
        st.session_state.selected_note_index = len(nb.notes)
        st.rerun()

    st.write("---")
    
    # render notes list
    if not nb.notes:
        st.info("Brak notatek. Dodaj pierwszą powyżej!")
    else:
        st.write("**Twoje notatki:**")
        note_options = {i: f"{n.title} ({n.date.strftime('%d/%m')})" for i, n in enumerate(nb.notes, start=1)}
        
        # determine the current index or default to the first one
        current_selection = st.session_state.selected_note_index if st.session_state.selected_note_index in note_options else 1
        
        selected_ui = st.radio(
            "Wybierz notatkę",
            options=list(note_options.keys()),
            format_func=lambda x: note_options[x],
            index=list(note_options.keys()).index(current_selection),
            label_visibility="collapsed"
        )
        st.session_state.selected_note_index = selected_ui

    # tag management
    st.write("---")
    with st.expander("Tagi"):
        new_tag = st.text_input("Dodaj nowy tag:")
        if st.button("Dodaj tag", use_container_width=True) and new_tag:
            nb.add_new_tag_to_system(new_tag)
            nb.save_to_json()
            st.rerun()
        
        st.write("**Dostępne tagi:**")
        st.caption(", ".join(sorted(nb.tags)) if nb.tags else "Brak")


# note edit panel
if nb.notes and st.session_state.selected_note_index:
    idx = st.session_state.selected_note_index
    current_note = nb.notes[idx - 1]

    col_meta, col_actions = st.columns([2, 1])
    
    with col_meta:
        st.caption(f"Utworzono: {current_note.date.strftime('%Y-%m-%d %H:%M')} | Modyfikowano: {current_note.modified_date.strftime('%Y-%m-%d %H:%M')}")
    
    # text inputs
    edited_title = st.text_input("Tytuł", value=current_note.title, label_visibility="collapsed")
    edited_content = st.text_area("Treść notatki...", value=current_note.content, height=300, label_visibility="collapsed")

    # note tagging    
    st.write("**Tagi tej notatki:**")
    available_tags = list(sorted(nb.tags))
    
    # ensure note tags are present in the pool 
    for t in current_note.tags:
        if t not in available_tags:
            available_tags.append(t)

    edited_tags = st.multiselect("Przypisz tagi", options=available_tags, default=current_note.tags, label_visibility="collapsed")

    # note actions
    st.write("---")
    btn_col1, btn_col2, btn_col3, _ = st.columns([1, 1, 1, 2])
    
    with btn_col1:
        if st.button("Zapisz zmiany", type="primary", use_container_width=True):
            nb.edit_note(idx, new_title=edited_title, new_content=edited_content)
            #wtf
            nb.notes[idx - 1].tags = edited_tags
            nb.save_to_json()
            st.success("Zapisano!")
            st.rerun()
            
    with btn_col2:
        email_recipient = st.text_input("Wyślij do:", value="przyklad@me.com", key="email_to", label_visibility="collapsed")
        if st.button("Wyślij mail", use_container_width=True):
            nb.send_mail(idx, email_recipient)
            
    with btn_col3:
        if st.button("Usuń", type="secondary", use_container_width=True):
            nb.delete_notes(idx)
            nb.save_to_json()
            st.session_state.selected_note_index = 1 if len(nb.notes) > 0 else None
            st.toast("Notatka usunięta")
            st.rerun()

else:
    # Empty State
    st.info("Witaj! Wybierz notatkę z paska bocznego lub kliknij 'Nowa notatka', aby rozpocząć pisanie.")