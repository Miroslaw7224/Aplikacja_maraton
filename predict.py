
import pandas as pd
from pycaret.regression import load_model, predict_model


#Funkcja do predykcji czasu półmaratonu (wiek, płeć, czas na 5 km)
def predict_time(sex: str, age: int, split_5k: str) -> str:
    """
    Przewiduje czas netto półmaratonu na podstawie płci, wieku i czasu na 5 km.
    Argumenty:
        sex (str): 'M' lub 'K'
        age (int): wiek zawodnika
        split_5k (str): czas na 5 km w formacie 'hh:mm:ss'
    Zwraca:
        str: przewidywany czas netto w formacie 'hh:mm:ss'
    """
    # Konwersja czasu 5 km do sekund
    try:
        h, m, s = map(int, split_5k.strip().split(":"))
        czas_5k_s = h * 3600 + m * 60 + s
    except:
        raise ValueError("Błędny format czasu – użyj hh:mm:ss")

    # Kodowanie płci
    sex_bin = 1 if sex.upper() == "M" else 0

    # Dane wejściowe
    df = pd.DataFrame([{
        "Wiek": age,
        "Płeć_bin": sex_bin,
        "5 km Czas (s)": czas_5k_s
    }])

    # Wczytanie modelu i predykcja
    model = load_model("model/model_polmaratonu")
    wynik = predict_model(model, data=df)
    total_seconds = int(wynik.loc[0, 'prediction_label'])

    # Formatowanie do hh:mm:ss
    godziny = total_seconds // 3600
    minuty = (total_seconds % 3600) // 60
    sekundy = total_seconds % 60
    return f"{godziny:02d}:{minuty:02d}:{sekundy:02d}"

#Funkcja do predykcji czasu półmaratonu na podstawie wieku i płci (model uproszczony)  
def predict_time_from_profile(sex: str, age: int) -> str:
    """
    Przewiduje czas netto półmaratonu na podstawie wieku i płci (model uproszczony).
    Argumenty:
        sex (str): 'M' lub 'K'
        age (int): wiek zawodnika
    Zwraca:
        str: przewidywany czas netto w formacie 'hh:mm:ss'
    """
    # Kodowanie płci
    sex_bin = 1 if sex.upper() == "M" else 0

    # Dane wejściowe
    df = pd.DataFrame([{
        "Wiek": age,
        "Płeć_bin": sex_bin
    }])

    # Wczytanie modelu profilowego i predykcja
    model = load_model("model/model_profilowy")
    wynik = predict_model(model, data=df)
    total_seconds = int(wynik.loc[0, 'prediction_label'])

    # Konwersja do formatu hh:mm:ss
    godziny = total_seconds // 3600
    minuty = (total_seconds % 3600) // 60
    sekundy = total_seconds % 60
    return f"{godziny:02d}:{minuty:02d}:{sekundy:02d}"