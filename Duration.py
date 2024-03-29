import os
from scipy.io import wavfile

folder_path = "Samples/Train_Delfin"


def czas_trwania(folder_path):
    for file in os.listdir(folder_path):
        duration_list = []
        file_path = os.path.join(folder_path, file)
        sr, data = wavfile.read(file_path)
        duration = str(len(data) / sr)

        duration_list.append(duration)
        for i in duration_list:
            print(f"Czas trwania {file}: " + i[:4] + " sekund")


def czas_trwania_pliku(folder_path, plik):
    duration_list = []
    file_path = os.path.join(folder_path, plik)
    sr, data = wavfile.read(file_path)
    duration = str(len(data) / sr)

    return duration


def znajdywanie_pliku(folder_path, plik):
    duration_list = []
    duration = czas_trwania_pliku(folder_path, plik)
    brak = True
    for file in os.listdir(folder_path):
        file = str(file)
        file_path = os.path.join(folder_path, file)

        if file.lower() == plik.lower():
                duration_list.append(duration)
                for i in duration_list:
                    print(f"Czas trwania {plik} wynosi {i[:4]} sekund")
                brak = False

    if brak:
        print("Nie znaleziono pliku")


def czasy_trwania_plikow(folder_path):
    plik = str(input("Podaj plik, który chcesz zmierzyć: "))
    lista = []
    lista.append(plik)
    brak = True
    while lista[0]:
        znajdywanie_pliku(folder_path, lista[0])
        lista.pop(0)
        nastepny = str(input("Podaj następny plik, który chcesz zmierzyć: "))
        lista.append(nastepny)


zadanie = input("Zmierzyć czas wszystkich plików - 1,\nZmierzyć czas jednego pliku - 2,\nDecyzja: ")
zadanie = int(zadanie)

if zadanie == 1:
    czas_trwania(folder_path)
elif zadanie == 2:
    czasy_trwania_plikow(folder_path)
