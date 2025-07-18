# 🏃‍♂️ Półmaraton AI Predictor

Aplikacja Streamlit do przewidywania czasu ukończenia półmaratonu na podstawie wieku, płci i (opcjonalnie) czasu na 5 km. Wykorzystuje modele ML oraz integrację z OpenAI i Langfuse.

---

## 📦 Wymagania
- Python 3.8+
- Pliki modeli w katalogu `model/`:
  - `model/model_polmaratonu.pkl`
  - `model/model_profilowy.pkl`
- Plik `requirements.txt` z zależnościami
- Klucze API do OpenAI i Langfuse

---

## ⚙️ Konfiguracja środowiska

1. **Klonuj repozytorium i przejdź do katalogu projektu:**
   ```bash
   git clone <adres-repo>
   cd Aplikacja_maraton
   ```

2. **Utwórz i aktywuj wirtualne środowisko (opcjonalnie):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   ```

3. **Zainstaluj zależności:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Przygotuj plik `.env` (lokalnie):**
   ```env
   OPENAI_API_KEY=sk-...
   LANGFUSE_PUBLIC_KEY=pk-...
   LANGFUSE_SECRET_KEY=sk-...
   LANGFUSE_HOST=https://cloud.langfuse.com
   ```
   > **Uwaga:** Na Digital Ocean App Platform dodaj te zmienne przez panel (Settings → Environment Variables).

5. **Upewnij się, że pliki modeli są w katalogu `model/`!**

---

## 🚀 Deployment na Digital Ocean App Platform

1. **Zaloguj się do Digital Ocean i utwórz nową aplikację (App Platform).**
2. **Wskaż repozytorium z projektem.**
3. **W sekcji "Build & Run" ustaw:**
   - **Build Command:** *(zostaw puste lub)*
   - **Run Command:**
     ```
     streamlit run app.py --server.port $PORT --server.address 0.0.0.0
     ```
4. **Dodaj zmienne środowiskowe w panelu (Settings → Environment Variables):**
   - `OPENAI_API_KEY`
   - `LANGFUSE_PUBLIC_KEY`
   - `LANGFUSE_SECRET_KEY`
   - `LANGFUSE_HOST`
5. **Upewnij się, że katalog `model/` z plikami .pkl jest w repozytorium!**
6. **Zatwierdź i uruchom aplikację.**

---

## 🖥️ Deployment na własnym serwerze (Droplet)

1. **Przenieś pliki projektu na serwer (np. przez SFTP lub git).**
2. **Zainstaluj zależności:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Utwórz plik `.env` na serwerze z kluczami jak wyżej.**
4. **Uruchom aplikację:**
   ```bash
   streamlit run app.py --server.port 80 --server.address 0.0.0.0
   ```
   > Jeśli port 80 jest zajęty, użyj np. 8501 i otwórz port w firewallu.

---

## 🛠️ Troubleshooting
- **Błąd: Brak kluczy API** – Upewnij się, że zmienne środowiskowe są ustawione.
- **Błąd: Model not found** – Sprawdź, czy pliki .pkl są w katalogu `model/` i ścieżki w `predict.py` są poprawne.
- **Błąd: Port already in use** – Zmień port lub zatrzymaj inny proces na tym porcie.
- **Błąd: ImportError** – Sprawdź, czy wszystkie zależności są w `requirements.txt` i zainstalowane.

---

## 📞 Kontakt
W razie problemów lub pytań – napisz issue lub skontaktuj się z autorem projektu. 