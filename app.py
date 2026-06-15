import streamlit as st
import datetime
from classes import Notebook, Note

st.set_page_config(page_title="Python Notes", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    /* Target and remove the Deploy button and options menu across all Streamlit versions */
    [data-testid="stDeploymentDropdown"], .stAppDeployButton, [data-testid="stMainMenu"] {
        display: none !important;
    }
    /* Keep the header container container tracking structural but fully see-through */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }
    /* Force persistent clean light mode styling */
    .stApp { background-color: #ffffff; }
    [data-testid="stSidebar"] {
        background-color: #f2f2f7 !important;
        border-right: 1px solid #e5e5ea;
    }
    h1 { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica; font-weight: 700; color: #1c1c1e; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE BACKEND IN SESSION STATE ---
if "notebook" not in st.session_state:
    st.session_state.notebook = Notebook("notatki.json", "tagi.json")
    st.session_state.notebook.load_from_json()

if "selected_note_index" not in st.session_state:
    st.session_state.selected_note_index = 1 if st.session_state.notebook.notes else None

nb = st.session_state.notebook

# Sync the radio widget's state with the master selection index before it gets instantiated
st.session_state.sidebar_radio = st.session_state.selected_note_index

# Callback function to eliminate radio button lag
def update_selection():
    st.session_state.selected_note_index = st.session_state.sidebar_radio

with st.sidebar:
    st.title("Notatnik")

    # add new note    
    if st.button("Nowa notatka", use_container_width=True):
        nb.add_note("Bez tytułu", "")
        nb.save_to_json()
        new_index = len(nb.notes)
        st.session_state.selected_note_index = new_index
        st.rerun()

    st.write("---")
    
    # render notes list
    if not nb.notes:
        st.info("Brak notatek. Dodaj pierwszą powyżej!")
    else:
        st.write("**Twoje notatki:**")
        note_options = {i: f"{n.title} ({n.date.strftime('%d/%m')})" for i, n in enumerate(nb.notes, start=1)}
        
        # determine the current index or default to the first one
        current_selection = st.session_state.selected_note_index
        if current_selection not in note_options and note_options:
            current_selection = list(note_options.keys())[0]
        
        st.radio(
            "Wybierz notatkę",
            options=list(note_options.keys()),
            format_func=lambda x: note_options[x],
            index=list(note_options.keys()).index(current_selection),
            label_visibility="collapsed",
            key="sidebar_radio",
            on_change=update_selection
        )

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

    col_meta, col_tags = st.columns([3, 2])
    
    with col_meta:
        st.caption(f"Utworzono: {current_note.date.strftime('%Y-%m-%d %H:%M')} | Modyfikowano: {current_note.modified_date.strftime('%Y-%m-%d %H:%M')}")
    
    with col_tags:
        # note tagging    
        available_tags = list(sorted(nb.tags))
        
        # ensure note tags are present in the pool 
        for t in current_note.tags:
            if t not in available_tags:
                available_tags.append(t)

        edited_tags = st.multiselect("Przypisz tagi", options=available_tags, default=current_note.tags, label_visibility="collapsed", placeholder="Przypisz tagi...")

    st.write("")
    
    # text inputs
    edited_title = st.text_input("Tytuł", value=current_note.title, label_visibility="collapsed")
    edited_content = st.text_area("Treść notatki...", value=current_note.content, height=350, label_visibility="collapsed")

    # note actions
    st.write("---")
    btn_save, email_input, email_btn, btn_delete, _ = st.columns([1.2, 1.8, 1.0, 1.0, 1.5])
    
    with btn_save:
        if st.button("Zapisz zmiany", type="primary", use_container_width=True):
            nb.edit_note(idx, new_title=edited_title, new_content=edited_content)
            #wtf
            nb.notes[idx - 1].tags = edited_tags
            nb.save_to_json()
            st.success("Zapisano!")
            st.rerun()
            
    with email_input:
        email_recipient = st.text_input("Wyślij do:", value="przyklad@me.com", key="email_to", label_visibility="collapsed")
        
    with email_btn:
        if st.button("Wyślij mail", use_container_width=True):
            nb.send_mail(idx, email_recipient)
            
    with btn_delete:
        if st.button("Usuń", type="secondary", use_container_width=True):
            nb.delete_notes(idx)
            nb.save_to_json()
            st.session_state.selected_note_index = 1 if len(nb.notes) > 0 else None
            st.toast("Notatka usunięta")
            st.rerun()

else:
    # Empty State
    st.info("Witaj! Wybierz notatkę z paska bocznego lub kliknij 'Nowa notatka', aby rozpocząć pisanie.")