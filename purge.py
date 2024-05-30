import os
import glob
from scipy.io import wavfile
import warnings
import shutil


def move_damaged_wav_files_to_trash(root_dir, trash_dir):
    if not os.path.exists(trash_dir):
        os.makedirs(trash_dir)

    damaged_files = []
    for wav_path in glob.iglob(f'{root_dir}/**/*.wav', recursive=True):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                wavfile.read(wav_path)
                if len(w) > 0:
                    for warn in w:
                        if "Reached EOF prematurely" in str(warn.message):
                            damaged_files.append(wav_path)
                            break
            except Exception as e:
                print(f"Error reading {wav_path}: {e}")
                damaged_files.append(wav_path)

    for file in damaged_files:
        try:
            print(f"Przenoszenie pliku: {file} do folderu {trash_dir}")
            shutil.move(file, trash_dir)
            print(f"Plik przeniesiony: {file}")
        except Exception as e:
            print(f"Error moving {file} to {trash_dir}: {e}")


def move_specific_file_to_trash(folder_choice, file_name, trash_dir):
    if not os.path.exists(trash_dir):
        os.makedirs(trash_dir)

    file_path = os.path.join(folder_choice, file_name)
    if os.path.exists(file_path):
        try:
            print(f"Przenoszenie pliku: {file_path} do folderu {trash_dir}")
            shutil.move(file_path, trash_dir)
            print(f"Plik przeniesiony: {file_path}")
        except Exception as e:
            print(f"Error moving {file_path} to {trash_dir}: {e}")
    else:
        print(f"Plik {file_path} nie istnieje.")


if __name__ == "__main__":
    root_directory = 'Samples/Humbak'
    trash_directory = 'Samples/Kosz'

    choice = input("Czy chcesz usunąć wszystkie uszkodzone pliki (tak/nie)? ").strip().lower()

    if choice == 'tak':
        move_damaged_wav_files_to_trash(root_directory, trash_directory)
    else:
        while True:
            folder_choice = input(
                "Wybierz folder:\n1. Samples/Train_Delfin\n2. Samples/Train_Humbak\nWybór (1/2): ").strip()
            if folder_choice == '1':
                folder_path = 'Samples/Train_Delfin'
            elif folder_choice == '2':
                folder_path = 'Samples/Train_Humbak'
            else:
                print("Nieprawidłowy wybór. Spróbuj ponownie.")
                continue

            specific_file = input("Podaj nazwę pliku WAV do usunięcia (lub wpisz 'stop', aby zakończyć): ").strip()
            if specific_file.lower() == 'stop':
                break
            move_specific_file_to_trash(folder_path, specific_file, trash_directory)

    print("Zakończone przenoszenie plików do kosza")
