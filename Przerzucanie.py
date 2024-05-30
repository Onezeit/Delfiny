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

    print(f"Pliki dłuższe niż {n} sekund: {number_files}")
    print(f"Wszystkich plików: {total_files}")

    if files:
        print("Pliki dłuższe niż podana liczba sekund:")
        for file in files:
            print(file)
        move_files = input("Czy chcesz przenieść te pliki? (tak/nie) ")
        if move_files.lower() == 'tak':
            specific_files = input("Czy chcesz przenieść wszystkie pliki, czy określoną liczbę? (wszystkie/liczba) ")
            if specific_files.lower() == 'wszystkie':
                move_files_longer_than_n_seconds(source_folder, target_folder, n, files)
            else:
                try:
                    num_files_to_move = int(specific_files)
                    if num_files_to_move > number_files:
                        num_files_to_move = number_files
                    move_files_longer_than_n_seconds(source_folder, target_folder, n, files[:num_files_to_move])
                except ValueError:
                    print("Podano nieprawidłową liczbę.")
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


source_folder = 'Samples/Train_Orka'
target_folder = 'Samples/Orka'

if source_folder:
    n = float(input("Podaj minimalny czas trwania plików audio: "))
    user_input = int(input(f"1 - Zobacz ile jest plików powyżej {n} sekund \n"
                           f"2 - Przerzuć wszystkie pliki, które mają powyżej {n} sekund \n"))

    if user_input == 1:
        files_longer_than_n_seconds(source_folder, target_folder, n)
    elif user_input == 2:
        files_to_move = [file for file in os.listdir(source_folder) if file.endswith('.wav')]
        specific_files = input("Czy chcesz przenieść wszystkie pliki, czy określoną liczbę? (wszystkie/liczba) ")
        if specific_files.lower() == 'wszystkie':
            move_files_longer_than_n_seconds(source_folder, target_folder, n, files_to_move)
        else:
            try:
                num_files_to_move = int(specific_files)
                if num_files_to_move > len(files_to_move):
                    num_files_to_move = len(files_to_move)
                move_files_longer_than_n_seconds(source_folder, target_folder, n, files_to_move[:num_files_to_move])
            except ValueError:
                print("Podano nieprawidłową liczbę.")
    else:
        print("Podano złą cyfrę")
