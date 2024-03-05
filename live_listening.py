import pyaudio
import requests
from bs4 import BeautifulSoup
import wave
import sys


def record_audio(output_filename, duration=25, channels=1, sample_rate=44100):
    p = pyaudio.PyAudio()

    # Ustawienia nagrywania
    format = pyaudio.paInt16
    frames_per_buffer = 1024

    # Rozpocznij nagrywanie
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


def get_website_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Błąd podczas pobierania strony. Kod statusu: {response.status_code}")
        return None


def main():
    url = "https://live.orcasound.net/listen/"
    print("1 - Orcasound Lab \n"
          "2 - North San Juan Channel \n"
          "3 - Port Townsend \n"
          "4 - Bush Point \n"
          "5 - Beach Camp at Sunset Bay \n"
          "6 - Point Robinson \n")
    choice = int(input("Choose station you want to probe sound from \n"))
    if choice == 1:
        key = "orcasound-lab"
    elif choice == 2:
        key = "north-sjc"
    elif choice == 3:
        key = "port-townsend"
    elif choice == 4:
        key = "bush-point"
    elif choice == 5:
        key = "sunset-bay"
    elif choice == 6:
        key = "point-robinson"
    else:
        print("Invalid number")

    website_url = url + key
    print(website_url)

    output_filename = "LiveSamples/output.wav"
    website_content = get_website_content(website_url)

    if website_content:
        record_audio(output_filename)


if __name__ == "__main__":
    main()
