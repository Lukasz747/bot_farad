import streamlit as st
import google.generativeai as genai
import os

# Ukrywanie logo/stopki Streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stAppDeployButton {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 1. Konfiguracja API
# 1. Konfiguracja API - bezpieczne pobieranie z sekretów
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. Funkcja ładująca wiedzę z pliku .md
def wczytaj_wiedze():
    with open("wiedza_farad.md", "r", encoding="utf-8") as f:
        return f.read()

wiedza = wczytaj_wiedze()

# 3. System Prompt z wstrzykniętą wiedzą
system_instruction = f"""
Jesteś profesjonalnym asystentem firmy Farad, prowadzonej przez Łukasza Drumlaka.
Twoja baza wiedzy: {wiedza}

Instrukcja: 
- Odpowiadaj rzeczowo, technicznie i uprzejmie.
- Używaj TYLKO informacji z bazy wiedzy. 
- Jeśli klient pyta o ceny, poproś o kontakt w celu wyceny indywidualnej.
- Zawsze podkreślaj profesjonalizm i dbałość o bezpieczeństwo.
- Jeśli czegoś nie wiesz, zachęć do kontaktu z Łukaszem Drumlakiem pod numerem 512255966.
"""

model = genai.GenerativeModel('gemini-3.1-flash-lite', system_instruction=system_instruction)

st.subheader("Farad - Twój Asystent Techniczny")

# Inicjalizacja czatu
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Obsługa czatu
if prompt := st.chat_input("W czym mogę pomóc?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = model.generate_content(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})