import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def symuluj_harmonogram(zadania):
  """
  Symuluje harmonogram zadań na jednej maszynie.
  Teraz zadania mają czasy dostępności.

  Args:
    zadania: Lista krotek, gdzie każda krotka reprezentuje zadanie
             i zawiera (czas_trwania, termin_wykonania, czas_dostepnosci).

  Returns:
    Lista permutacji zadań.
  """
  n = len(zadania)
  permutacje = list(range(n))
  random.shuffle(permutacje)
  return permutacje

def oblicz_funkcje_celu(permutacja, zadania):
  """
  Oblicza funkcję celu (np. maksymalne opóźnienie) dla danej permutacji,
  uwzględniając czasy dostępności.

  Args:
    permutacja: Lista indeksów zadań w określonej kolejności.
    zadania: Lista krotek z informacjami o zadaniach
             (czas_trwania, termin_wykonania, czas_dostepnosci).

  Returns:
    Wartość funkcji celu (maksymalne opóźnienie).
  """
  czas_zakonczenia_poprzedniego = 0
  maksymalne_opoznienie = 0
  for i in permutacja:
    czas_trwania, termin_wykonania, czas_dostepnosci = zadania[i]

    # Czas rozpoczęcia to maksimum z czasu zakończenia poprzedniego zadania
    # i czasu dostępności bieżącego zadania
    czas_start = max(czas_zakonczenia_poprzedniego, czas_dostepnosci)

    czas_zakonczenia_biezacego = czas_start + czas_trwania
    opoznienie = max(0, czas_zakonczenia_biezacego - termin_wykonania)
    maksymalne_opoznienie = max(maksymalne_opoznienie, opoznienie)

    czas_zakonczenia_poprzedniego = czas_zakonczenia_biezacego # Aktualizacja dla następnej iteracji

  return maksymalne_opoznienie

def wizualizuj_harmonogram(permutacja, zadania):
  """
  Wizualizuje harmonogram zadań za pomocą wykresu Gantta,
  uwzględniając czasy dostępności.

  Args:
    permutacja: Lista indeksów zadań w określonej kolejności.
    zadania: Lista krotek z informacjami o zadaniach
             (czas_trwania, termin_wykonania, czas_dostepnosci).
  """
  df = []
  czas_zakonczenia_poprzedniego = 0
  for i in permutacja:
    czas_trwania, termin_wykonania, czas_dostepnosci = zadania[i]

    # Obliczanie czasu startu i końca dla wizualizacji
    czas_start = max(czas_zakonczenia_poprzedniego, czas_dostepnosci)
    czas_koniec = czas_start + czas_trwania

    df.append(
        {
            "Zadanie": f"Zadanie {i+1} (RT={czas_dostepnosci})", # Dodajemy info o RT do etykiety
            "Start": czas_start,
            "Koniec": czas_koniec,
            "Termin": termin_wykonania,
            "Dostępność": czas_dostepnosci, # Dodajemy dla ewentualnej innej wizualizacji
        }
    )
    czas_zakonczenia_poprzedniego = czas_koniec # Aktualizacja

  df = pd.DataFrame(df)

  fig, ax = plt.subplots(figsize=(12, 6)) # Zwiększamy trochę rozmiar

  # Wykres Gantta (paski zadań)
  # Rysujemy pełny pasek od startu do końca
  for index, row in df.iterrows():
      ax.barh(row["Zadanie"], row["Koniec"] - row["Start"], left=row["Start"], color='skyblue', label='Czas trwania' if index == 0 else "")

  # Linie terminów wykonania
  for _, row in df.iterrows():
      ax.axvline(
          x=row["Termin"],
          ymin=df.index.get_loc(_) / len(df), # Pozycja ymin
          ymax=(df.index.get_loc(_) + 1) / len(df), # Pozycja ymax
          color="red",
          linestyle="--",
          label="Termin wykonania" if _ == 0 else "",
      )

  # Opcjonalnie: oznaczenie czasów dostępności na osi czasu
  # for _, row in df.iterrows():
  #      ax.plot(row["Dostępność"], row["Zadanie"], 'go', markersize=5, label='Czas dostępności' if _ == 0 else "")


  ax.set_xlabel("Czas")
  ax.set_ylabel("Zadanie")
  ax.set_title("Wizualizacja Harmonogramu Zadań z Czasami Dostępności (RT)")

  # Usuń duplikaty z legendy
  handles, labels = plt.gca().get_legend_handles_labels()
  by_label = dict(zip(labels, handles))
  ax.legend(by_label.values(), by_label.keys())

  plt.tight_layout() # Poprawia ułożenie elementów
  plt.show()


# === Przykład użycia ===
# (czas_trwania, termin_wykonania, czas_dostepnosci)
zadania = [(3, 10, 0), (2, 8, 2), (5, 12, 1), (1, 5, 4)]

# Prosta symulacja - szukanie najlepszej permutacji
najlepsza_permutacja = None
min_opoznienie = float('inf') # Inicjalizacja dużą wartością

# Sprawdzenie wszystkich permutacji (dla małej liczby zadań)
# Dla większej liczby zadań potrzebny byłby bardziej zaawansowany algorytm
import itertools
n = len(zadania)
permutacje_wszystkie = list(itertools.permutations(range(n)))

print(f"Liczba możliwych permutacji: {len(permutacje_wszystkie)}")

for permutacja in permutacje_wszystkie:
    opoznienie = oblicz_funkcje_celu(permutacja, zadania)
    #print(f"Permutacja: {permutacja}, Opóźnienie: {opoznienie}") # Do debugowania
    if opoznienie < min_opoznienie:
        min_opoznienie = opoznienie
        najlepsza_permutacja = list(permutacja) # Przechowujemy jako listę

# Jeśli nie znaleziono żadnej permutacji (co nie powinno się zdarzyć przy itertools)
if najlepsza_permutacja is None and zadania:
    najlepsza_permutacja = list(range(n))
    min_opoznienie = oblicz_funkcje_celu(najlepsza_permutacja, zadania)


print("\n--- Wynik Optymalizacji ---")
if najlepsza_permutacja:
    print(f"Najlepsza znaleziona permutacja (indeksy zadań): {najlepsza_permutacja}")
    print(f"Kolejność zadań (ID): {[x+1 for x in najlepsza_permutacja]}")
    print(f"Minimalne maksymalne opóźnienie: {min_opoznienie}")

    # Wizualizacja najlepszego harmonogramu
    wizualizuj_harmonogram(najlepsza_permutacja, zadania)
else:
    print("Nie znaleziono rozwiązania.")