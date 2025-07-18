import streamlit as st
from predict import predict_time, predict_time_from_profile
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from langfuse import get_client
import uuid


# Inicjalizacja
load_dotenv()
langfuse = get_client()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.set_page_config(page_title="Półmaraton AI", layout="centered", page_icon="🏃‍♂️")


# 🔍 Funkcja do zgadywania płci z imienia
def infer_gender_from_name(name: str) -> str | None:
    if not name:
        return None
    name = name.strip().lower()
    if name.endswith("a") and name not in ["kuba", "barnaba", "ilia"]:
        return "K"
    return "M"


# 🧠 Funkcja do ekstrakcji danych z opisu tekstowego
def extract_user_data(prompt_text: str):
    try:
        with langfuse.start_as_current_span(name="🧠 Ekstrakcja danych z opisu") as span:
            system_prompt = (
                "Ekstrahuj dane użytkownika do formatu JSON. "
                "Format: {\"age\": int, \"sex\": \"M\" lub \"K\" (opcjonalnie), "
                "\"name\": str (opcjonalnie), \"pace_5k\": \"hh:mm:ss\" (opcjonalnie)}. "
                "Zwróć tylko poprawny JSON, bez komentarzy i żadnego dodatkowego tekstu."
            )
            with langfuse.start_as_current_generation(
                name="LLM: ekstrakcja danych",
                model="gpt-3.5-turbo",
                input=prompt_text
            ) as gen:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt_text}
                    ],
                    temperature=0
                )
                content = response.choices[0].message.content
                gen.update(output=content)
                if not content:
                    st.error("❌ Brak odpowiedzi od modelu OpenAI.")
                    gen.score(name="ekstrakcja", value=0)
                    return None
                data = json.loads(content)
                # Próbuj wywnioskować płeć z imienia
                if not data.get("sex") and data.get("name"):
                    guessed = infer_gender_from_name(data["name"])
                    if guessed:
                        data["sex"] = guessed
                        st.info(f"🤖 Płeć określona na podstawie imienia **{data['name']}**: {guessed}")
                gen.score(name="ekstrakcja", value=1.0)
                return data
    except Exception as e:
        st.error(f"❌ Błąd ekstrakcji danych: {e}")
        return None



# 🏁 Nagłówki
with st.container():
    st.markdown("""
        <h1 style='text-align: center; font-size: 42px; color: #f9fafb;'>A I  🧠 P R E D I C T O R</h1>
        <h1 style='text-align: center; font-size: 42px; color: #f9fafb;'>Zaplanuj swój maraton</h1>
        <hr style='border: 1px solid gray;'/>
    """, unsafe_allow_html=True)

# 💬 Pole tekstowe
st.markdown("### 💬 Powiedz mi coś o sobie i swoich wynikach")
tekst_input = st.text_area("Wpisz wiek, płeć, jeśli masz jakieś rekordy podziel się z nami (np. 5 km w 27 minut)", height=120)
extracted_data = None

if st.button("🤖 Zinterpretuj opis i przewiduj"):
    if not tekst_input.strip():
        st.warning("🟡 Pole opisu jest puste.")
    else:
        with st.spinner("⏳ Analizuję opis..."):
            extracted_data = extract_user_data(tekst_input)
            if extracted_data:
                tekst_age = extracted_data.get("age")
                tekst_sex = extracted_data.get("sex")
                tekst_pace = extracted_data.get("pace_5k", None)

                if not tekst_age or not tekst_sex:
                    st.error("❗ Nie udało się rozpoznać wieku lub płci.")
                else:
                    try:
                        if tekst_pace:
                            st.toast("✅ Wykryto dane do modelu: **wiek + płeć + czas 5 km**")
                            wynik = predict_time(tekst_sex.upper(), tekst_age, tekst_pace)
                        else:
                            st.toast("✅ Wykryto dane do modelu: **wiek + płeć**")
                            wynik = predict_time_from_profile(tekst_sex.upper(), tekst_age)

                        st.markdown(" ")
                        st.success(f"⏱️ Przewidywany czas netto: **{wynik}**")

                    except Exception as e:
                        st.error(f"❌ Wystąpił błąd predykcji: {e}")


# 📄 Ankieta
st.markdown("### 📄 Opcjonalnie skorzystaj z naszej krótkiej ankiety")
with st.expander("🧩 Tryb predykcji", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        opcja1 = st.checkbox("🧍 Wiek + płeć", key="opcja1")
    with col2:
        opcja2 = st.checkbox("🏃 Wiek + płeć + czas 5 km", key="opcja2")

    if opcja1 and opcja2:
        st.warning("❗ Możesz zaznaczyć tylko jedną opcję.")
        tryb = None
    elif opcja1:
        tryb = "Wiek + płeć"
    elif opcja2:
        tryb = "Wiek + płeć + czas 5 km"
    else:
        tryb = None


# 🧍 Dane użytkownika
with st.expander("🧍‍♂️ Dane zawodnika", expanded=True):
    form_age = st.slider("🎂 Wiek", 10, 99, 30)

    col1, col2 = st.columns(2)
    with col1:
        kobieta = st.checkbox("🙋‍♀️ Kobieta", value=False)
    with col2:
        mezczyzna = st.checkbox("🙋‍♂️ Mężczyzna", value=True)

    form_sex = None
    if kobieta and not mezczyzna:
        form_sex = "K"
    elif mezczyzna and not kobieta:
        form_sex = "M"
    elif kobieta and mezczyzna:
        st.warning("❗ Zaznacz tylko jedną płeć.")
    else:
        st.warning("❗ Zaznacz płeć.")

    if tryb == "Wiek + płeć + czas 5 km":
        st.markdown("### ⏱️ Czas na 5 km")
        c1, c2, c3 = st.columns(3)
        with c1:
            godziny = st.number_input("🕐 Godziny", 0, 5, 0)
        with c2:
            minuty = st.number_input("🕑 Minuty", 0, 59, 27)
        with c3:
            sekundy = st.number_input("🕒 Sekundy", 0, 59, 0)
        form_pace = f"{int(godziny):02}:{int(minuty):02}:{int(sekundy):02}"
    else:
        form_pace = None

st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)


# 🎯 PRZYCISK PREDYKCJI
if st.button("🎯 Oblicz przewidywany czas"):
    if tryb and form_sex:
        try:
            if tryb == "Wiek + płeć + czas 5 km" and form_pace:
                wynik = predict_time(form_sex.upper(), form_age, form_pace)
            elif tryb == "Wiek + płeć":
                wynik = predict_time_from_profile(form_sex.upper(), form_age)
            else:
                st.warning("❗ Brakuje danych – sprawdź formularz.")
                wynik = None

            if wynik:
                st.success(f"⏱️ Przewidywany czas ukończenia maratonu: **{wynik}**")
                st.balloons()  # 🎈
        except Exception as e:
            st.error(f"❌ Wystąpił błąd predykcji: {e}")

    elif tekst_input and not tryb:
        st.info("ℹ️ Dane zostaną odczytane z pola tekstowego.")
        extracted_data = extract_user_data(tekst_input)
        if extracted_data:
            try:
                wynik = None
                if extracted_data.get("pace_5k"):
                    wynik = predict_time(extracted_data["sex"].upper(), extracted_data["age"], extracted_data["pace_5k"])
                else:
                    wynik = predict_time_from_profile(extracted_data["sex"].upper(), extracted_data["age"])
                st.success(f"⏱️ Przewidywany czas ukończenia maratonu: **{wynik}**")
                st.balloons()  # 🎈
            except Exception as e:
                st.error(f"❌ Wystąpił błąd: {e}")
    else:
        st.error("❗ Podaj dane – w ankiecie lub w opisie.")
