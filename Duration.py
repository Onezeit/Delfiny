import os
from scipy.io import wavfile

folder_path = "Samples/Train_Orka"


def czas_trwania(folder_path):
    files = os.listdir(folder_path)

    duration_list = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        sr, data = wavfile.read(file_path)
        duration = str(len(data) / sr)
        duration_list.append(duration)
        print(f"Czas trwania {file}: {duration[:4]} sekund")

    print(f"Liczba plików w folderze {folder_path}: {len(files)}")


def czas_trwania_pliku(folder_path, plik):
    file_path = os.path.join(folder_path, plik)
    sr, data = wavfile.read(file_path)
    duration = str(len(data) / sr)
    return duration


def znajdywanie_pliku(folder_path, plik):
    duration = czas_trwania_pliku(folder_path, plik)
    brak = True
    for file in os.listdir(folder_path):
        if file.lower() == plik.lower():
            print(f"Czas trwania {plik} wynosi {duration[:4]} sekund")
            brak = False
            break
    if brak:
        print("Nie znaleziono pliku")


def czasy_trwania_plikow(folder_path):
    while True:
        plik = str(input("Podaj plik, który chcesz zmierzyć (lub wpisz 'stop' aby zakończyć): "))
        if plik.lower() == 'stop':
            break
        znajdywanie_pliku(folder_path, plik)


zadanie = input("Zmierzyć czas wszystkich plików - 1,\nZmierzyć czas jednego pliku - 2,\nDecyzja: ")
zadanie = int(zadanie)

if zadanie == 1:
    czas_trwania(folder_path)
elif zadanie == 2:
    czasy_trwania_plikow(folder_path)
