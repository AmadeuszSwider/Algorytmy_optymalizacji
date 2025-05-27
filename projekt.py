import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

# === IMPLEMENTACJA PROBLEMU RPQ ===

def symuluj_harmonogram(zadania):
    n = len(zadania)
    permutacje = list(range(n))
    random.shuffle(permutacje)
    return permutacje

def oblicz_funkcje_celu(permutacja, zadania):
    czas_zakonczenia_poprzedniego = 0
    maksymalne_opoznienie = 0
    for i in permutacja:
        czas_trwania, termin_wykonania, czas_dostepnosci = zadania[i]
        czas_start = max(czas_zakonczenia_poprzedniego, czas_dostepnosci)
        czas_zakonczenia_biezacego = czas_start + czas_trwania
        opoznienie = max(0, czas_zakonczenia_biezacego - termin_wykonania)
        maksymalne_opoznienie = max(maksymalne_opoznienie, opoznienie)
        czas_zakonczenia_poprzedniego = czas_zakonczenia_biezacego
    return maksymalne_opoznienie

def oblicz_statystyki_opoznien(permutacja, zadania):
    czas_zakonczenia_poprzedniego = 0
    opoznienia = []
    for i in permutacja:
        czas_trwania, termin_wykonania, czas_dostepnosci = zadania[i]
        czas_start = max(czas_zakonczenia_poprzedniego, czas_dostepnosci)
        czas_zakonczenia_biezacego = czas_start + czas_trwania
        opoznienie = max(0, czas_zakonczenia_biezacego - termin_wykonania)
        opoznienia.append(opoznienie)
        czas_zakonczenia_poprzedniego = czas_zakonczenia_biezacego

    maksymalne = max(opoznienia) if opoznienia else 0
    srednie = sum(opoznienia) / len(opoznienia) if opoznienia else 0
    suma = sum(opoznienia)
    return maksymalne, srednie, suma

def wyswietl_zadania(zadania):
    print("Lista zadań (czas_trwania, termin_wykonania, czas_dostepnosci):")
    for idx, zadanie in enumerate(zadania, start=1):
        print(f"  Zadanie {idx}: {zadanie}")

def wizualizuj_harmonogram(permutacja, zadania):
    df = []
    czas_zakonczenia_poprzedniego = 0
    for idx, i in enumerate(permutacja):
        czas_trwania, termin_wykonania, czas_dostepnosci = zadania[i]
        czas_start = max(czas_zakonczenia_poprzedniego, czas_dostepnosci)
        czas_koniec = czas_start + czas_trwania
        opoznienie = max(0, czas_koniec - termin_wykonania)
        df.append({
            "Zadanie": f"Zadanie {i+1} (RT={czas_dostepnosci})",
            "Start": czas_start,
            "Koniec": czas_koniec,
            "Termin": termin_wykonania,
            "Opoznione": opoznienie > 0
        })
        czas_zakonczenia_poprzedniego = czas_koniec

    df = pd.DataFrame(df)

    fig, ax = plt.subplots(figsize=(12, 6))
    for idx, row in df.iterrows():
        kolor = 'lightcoral' if row["Opoznione"] else 'skyblue'
        ax.barh(y=idx, width=row["Koniec"] - row["Start"], left=row["Start"], color=kolor)
        ax.text(row["Start"] + 0.1, idx, f"{int(row['Start'])}-{int(row['Koniec'])}", va='center', fontsize=8)

    for idx, row in df.iterrows():
        ax.vlines(x=row["Termin"], ymin=idx - 0.4, ymax=idx + 0.4, color="red", linestyle="--")

    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df["Zadanie"])
    ax.set_xlabel("Czas")
    ax.set_ylabel("Zadanie")
    ax.set_title("Wizualizacja Harmonogramu Zadań (Kolor = Opóźnienie)")
    plt.tight_layout()
    plt.show()

# === ALGORYTM SYMULOWANEGO WYŻARZANIA ===

def simulated_annealing(zadania, temp_poczatkowa=1000, wsp_chlodzenia=0.95, min_temp=1, max_iter=1000):
    n = len(zadania)
    aktualne_rozw = symuluj_harmonogram(zadania)
    aktualny_koszt = oblicz_funkcje_celu(aktualne_rozw, zadania)
    najlepsze_rozw = list(aktualne_rozw)
    najlepszy_koszt = aktualny_koszt

    T = temp_poczatkowa
    historia_temperatur = [T]
    historia_kosztow = [najlepszy_koszt]

    while T > min_temp:
        for _ in range(max_iter):
            i, j = random.sample(range(n), 2)
            sasiad = list(aktualne_rozw)
            sasiad[i], sasiad[j] = sasiad[j], sasiad[i]
            koszt_sasiada = oblicz_funkcje_celu(sasiad, zadania)

            delta = koszt_sasiada - aktualny_koszt
            if delta < 0 or random.random() < math.exp(-delta / T):
                aktualne_rozw = sasiad
                aktualny_koszt = koszt_sasiada
                if aktualny_koszt < najlepszy_koszt:
                    najlepsze_rozw = list(aktualne_rozw)
                    najlepszy_koszt = aktualny_koszt

            historia_kosztow.append(najlepszy_koszt)
            historia_temperatur.append(T)

        T *= wsp_chlodzenia

    return najlepsze_rozw, najlepszy_koszt, historia_temperatur, historia_kosztow

# === GENEROWANIE PRZYKŁADOWYCH DANYCH ===

def generuj_zadania(n):
    zadania = []
    for _ in range(n):
        r = random.randint(0, 10)
        p = random.randint(1, 6)
        bufor = random.randint(n // 2, n + 5)
        d = r + p + bufor
        zadania.append((p, d, r))
    return zadania

# === URUCHOMIENIE ===

if __name__ == "__main__":
    random.seed(42)

    zadania = generuj_zadania(10)
    wyswietl_zadania(zadania)

    perm, koszt, historia_T, historia_C = simulated_annealing(zadania)

    print("\n--- Najlepsze rozwiązanie ---")
    print("Permutacja:", perm)
    print("Koszt (maksymalne opóźnienie):", koszt)

    maks_opoz, sred_opoz, suma_opoz = oblicz_statystyki_opoznien(perm, zadania)
    print(f"Statystyki opóźnień:\n  Maksymalne: {maks_opoz}\n  Średnie: {sred_opoz:.2f}\n  Suma: {suma_opoz}")

    wizualizuj_harmonogram(perm, zadania)

    # Wykres zmian temperatury i kosztu
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(historia_T, 'r-', label='Temperatura')
    ax2.plot(historia_C, 'b-', label='Koszt')
    ax1.set_xlabel('Iteracja')
    ax1.set_ylabel('Temperatura', color='r')
    ax2.set_ylabel('Koszt', color='b')
    plt.title("Ewolucja temperatury i najlepszego kosztu")
    fig.tight_layout()
    plt.show()
