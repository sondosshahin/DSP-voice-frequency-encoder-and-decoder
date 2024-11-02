import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import simpleaudio as sa
import wave
from scipy.fft import fft

# Encoding frequencies for each English character
encoding_frequencies = {
    'a': (100, 1100, 2500),
    'b': (100, 1100, 3000),
    'c': (100, 1100, 3500),
    'd': (100, 1300, 2500),
    'e': (100, 1300, 3000),
    'f': (100, 1300, 3500),
    'g': (100, 1500, 2500),
    'h': (100, 1500, 3000),
    'i': (100, 1500, 3500),
    'j': (300, 1100, 2500),
    'k': (300, 1100, 3000),
    'l': (300, 1100, 3500),
    'm': (300, 1300, 2500),
    'n': (300, 1300, 3000),
    'o': (300, 1300, 3500),
    'p': (300, 1500, 2500),
    'q': (300, 1500, 3000),
    'r': (300, 1500, 3500),
    's': (500, 1100, 2500),
    't': (500, 1100, 3000),
    'u': (500, 1100, 3500),
    'v': (500, 1300, 2500),
    'w': (500, 1300, 3000),
    'x': (500, 1300, 3500),
    'y': (500, 1500, 2500),
    'z': (500, 1500, 3000),
    ' ': (500, 1500, 3500)
}

# Duration of each character signal in milliseconds
character_duration = 40

# New sampling frequency (Fs)
Fs = 8000

class DecoderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Decoder")

        self.label = ttk.Label(root, text="Select an audio file to decode:")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.file_entry = ttk.Entry(root, width=40)
        self.file_entry.grid(row=1, column=0, columnspan=2, pady=10)

        self.browse_button = ttk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=1, column=2, pady=10)

        self.decode_button = ttk.Button(root, text="Decode", command=self.decode)
        self.decode_button.grid(row=2, column=0, columnspan=3, pady=10)

        self.result_label = ttk.Label(root, text="")
        self.result_label.grid(row=3, column=0, columnspan=3, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def decode(self):
        if self.file_entry.get():
            encoded_signal = load_audio(self.file_entry.get())
            print(encoded_signal)
            decoded_string = decode_signal(encoded_signal)
            self.result_label["text"] = "Decoded String: " + decoded_string
        else:
            self.result_label["text"] = "Please select an audio file."

def load_audio(file_path):
    wf = wave.open(file_path, 'rb')
    signal = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
    wf.close()
    return signal

def decode_signal(encoded_signal):
    decoded_string = ""
    for i in range(0, len(encoded_signal), int(Fs * character_duration / 1000)):
        segment = encoded_signal[i:i + int(Fs * character_duration / 1000)]
        frequencies = get_frequencies(segment)
        frequencies = np.sort(frequencies)
        print(frequencies)
        decoded_char = get_decoded_char(frequencies)
        decoded_string += decoded_char
    return decoded_string

def get_frequencies(segment):
    # Compute Fourier Transform to get frequency components
    spectrum = fft(segment)
    # Extract the frequencies and their corresponding amplitudes
    frequencies = np.fft.fftfreq(len(spectrum), 1 / Fs)
    amplitude = np.abs(spectrum)
    # Keep only positive frequencies
    positive_freq_mask = frequencies > 0
    frequencies = frequencies[positive_freq_mask]
    amplitude = amplitude[positive_freq_mask]
    # Get the top 3 frequencies with the highest amplitudes
    top_frequencies = frequencies[np.argsort(amplitude)[-3:]]
    return top_frequencies

def get_decoded_char(frequencies):
    # Find the closest encoding frequency to the detected frequencies
    min_distance = float('inf')
    decoded_char = ' '
    for char, encoding_freqs in encoding_frequencies.items():
        distance = np.sum(np.abs(np.array(frequencies) - np.array(encoding_freqs)))
        if distance < min_distance:
            min_distance = distance
            decoded_char = char
    return decoded_char

if __name__ == "__main__":
    root = tk.Tk()
    app = DecoderApp(root)
    root.mainloop()
