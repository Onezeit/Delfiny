from scipy.io import wavfile
import os
import shutil


def files_longer_than_n_seconds(source_folder, target_folder, n):
    total_files = 0
    number_files = 0
    files = []

    for filename in os.listdir(source_folder):
        if filename.endswith('.wav'):
            file_path = os.path.join(source_folder, filename)
            try:
                sr, data = wavfile.read(file_path)
                duration = len(data) / sr
                if duration > n:
                    number_files += 1
                    files.append(filename)
            except Exception as e:
                print(f"Problem z plikiem {filename}: {e}")
            total_files += 1

    if files:
        print("Pliki dłuższe niż podana liczba sekund:")
        for file in files:
            print(file)
        print(f"Wszystkich plików: {total_files}")
        print(f"Pliki dłuższe niż {n} sekund: {number_files}")
        move_files = input("Czy chcesz przenieść te pliki? (tak/nie) ")
        if move_files.lower() == 'tak':
            move_files_longer_than_n_seconds(source_folder, target_folder, n, files)
    else:
        print(f"Żadne pliki nie są dłuższe niż {n} sekund.")


def move_files_longer_than_n_seconds(source_folder, target_folder, n, files_to_move):
    files_moved = 0

    for filename in files_to_move:
        file_path = os.path.join(source_folder, filename)
        try:
            sr, data = wavfile.read(file_path)
            duration = len(data) / sr
            if duration > n:
                shutil.move(file_path, os.path.join(target_folder, filename))
                print(f"Przeniesiono: {filename}")
                files_moved += 1

        except Exception as e:
            print(f"Problem z przeniesieniem pliku {filename}: {e}")

    if files_moved > 0:
        print(f"Przeniesiono plików: {files_moved}")
    else:
        print("Żadne pliki nie zostały przemieszczone.")


source_folder = 'Samples/Humbak'
target_folder = 'Samples/Train_Humbak'

if source_folder:
    n = float(input("Podaj minimalny czas trwania plików audio: "))
    user_input = int(input(f"1 - Zobacz ile jest plików powyżej {n} sekund \n"
                           f"2 - Przerzuć wszystkie pliki, które mają powyżej {n} sekund \n"))

if user_input == 1:
    files_longer_than_n_seconds(source_folder, target_folder, n)
elif user_input == 2:
    move_files_longer_than_n_seconds(source_folder, target_folder, n, os.listdir(source_folder))
else:
    print("Podano złą cyfrę")
