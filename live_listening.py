import tkinter as tk
import pyaudio
import requests
from bs4 import BeautifulSoup
import wave
from spectr_industrial import generator


def map_choice_to_key(option):
    mapping = {
        "Orcasound Lab": "orcasound-lab",
        "North San Juan Channel": "north-sjc",
        "Port Townsend": "port-townsend",
        "Bush Point": "bush-point",
        "Beach Camp at Sunset Bay": "sunset-bay",
        "Point Robinson": "point-robinson",
    }

    selected_option_text = option.split(" - ")[1]

    return mapping.get(selected_option_text)


def record_audio(output_filename, duration=10, channels=1, sample_rate=44100):
    p = pyaudio.PyAudio()

    format = pyaudio.paInt16
    frames_per_buffer = 1024

    stream = p.open(format=format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=frames_per_buffer)

    print("Nagrywanie rozpoczęte...")

    frames = []
    for i in range(0, int(sample_rate / frames_per_buffer * duration)):
        data = stream.read(frames_per_buffer)
        frames.append(data)

    print("Nagrywanie zakończone.")

    # Zakończ nagrywanie i zapisz do pliku WAV
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    print(f"Nagranie zapisane jako {output_filename}")

    # Po nagraniu uruchom funkcję spektogram z nagranym dźwiękiem
    generator(output_filename)


def get_website_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Błąd podczas pobierania strony. Kod statusu: {response.status_code}")
        return None


def map_choice_to_key(option):
    mapping = {
        "Orcasound Lab": "orcasound-lab",
        "North San Juan Channel": "north-sjc",
        "Port Townsend": "port-townsend",
        "Bush Point": "bush-point",
        "Beach Camp at Sunset Bay": "sunset-bay",
        "Point Robinson": "point-robinson",
    }

    # Get the selected option text
    selected_option_text = option.split(" - ")[1]

    return mapping.get(selected_option_text)


def select_option(option, selected_option_label, recording_info_text):
    selected_option_label.config(text=f"Wybrano opcję: {option}")

    # Pobierz klucz na podstawie opcji
    key = map_choice_to_key(option)

    # Wywołaj funkcję z odpowiednimi argumentami
    url = "https://live.orcasound.net/listen/"
    website_url = url + key
    get_website_content(website_url)  # Zakładam, że ta funkcja zdefiniowana jest w live_listening

    # Dodaj kod rozpoczynający nagrywanie
    output_filename = "output.wav"
    record_audio(output_filename)

    # Aktualizuj pole tekstowe z informacjami dotyczącymi nagrywania
    recording_info_text.config(state=tk.NORMAL)
    recording_info_text.insert(tk.END, f"\nNagrywanie zakończone. Plik zapisany jako {output_filename}\n")
    recording_info_text.config(state=tk.DISABLED)


def start_recording(recording_label):
    # Tutaj umieść kod do rozpoczęcia nagrywania, na przykład wywołanie funkcji do nagrywania dźwięku.

    # Po zakończeniu nagrywania, możesz zaktualizować etykietę tekstu lub wyświetlić nowe okno z informacją.
    recording_label.config(text="Nagrywanie...")


def create_gui():
    root = tk.Tk()
    root.title("Nagrywacz")
    root.geometry("800x500")  # Proporcje 16:9

    # Etykieta informacyjna
    info_label = tk.Label(root, text="Wybierz jedną z poniższych stacji nasłuchujących:")
    info_label.pack(pady=10)

    # Lista opcji
    options = ["1 - Orcasound Lab", "2 - North San Juan Channel", "3 - Port Townsend", "4 - Bush Point", "5 - Beach Camp at Sunset Bay", "6 - Point Robinson"]

    # Tworzenie przycisków dla każdej opcji o równych rozmiarach
    option_buttons = []
    for option in options:
        button = tk.Button(root, text=option, command=lambda opt=option: select_option(opt, selected_option_label, recording_info_text), width=20, height=2)
        button.pack(pady=5)
        option_buttons.append(button)

    # Pole tekstowe z informacjami dotyczącymi nagrywania
    recording_info_text = tk.Text(root, height=10, width=60)
    recording_info_text.pack(pady=10)
    recording_info_text.insert(tk.END, "Informacje dotyczące nagrywania: \n")
    recording_info_text.config(state=tk.DISABLED)

    # Etykieta do wyświetlania wybranej opcji
    selected_option_label = tk.Label(root, text="")
    selected_option_label.pack()

    root.mainloop()


if __name__ == "__main__":
    create_gui()
