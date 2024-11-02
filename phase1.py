import tkinter as tk
from tkinter import ttk
import numpy as np
import simpleaudio as sa
import wave

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

# New sampling frequency (Fs)
Fs = 8000

class EncoderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Encoder")

        self.label = ttk.Label(root, text="Enter a string to encode:")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.entry = ttk.Entry(root, width=40)
        self.entry.grid(row=1, column=0, columnspan=2, pady=10)

        self.play_button = ttk.Button(root, text="Play", command=self.play)
        self.play_button.grid(row=2, column=0, pady=10)

        self.save_button = ttk.Button(root, text="Save as .wav", command=self.save)
        self.save_button.grid(row=2, column=1, pady=10)

    def play(self):
        input_string = self.entry.get()
        encoded_signal = encode_string(input_string)
        play_audio(encoded_signal)

    def save(self):
        input_string = self.entry.get()
        encoded_signal = encode_string(input_string)
        filename = "encoded_signal.wav"
        save_audio(encoded_signal, filename)

def encode_string(input_string):
    encoded_signal = np.array([], dtype=np.int16)

    for char in input_string.lower():
        frequencies = encoding_frequencies.get(char, encoding_frequencies[' '])  # Use space frequencies for unknown characters
        signal = generate_audio_signal(frequencies)
        encoded_signal = np.concatenate((encoded_signal, signal))

    return encoded_signal

def generate_audio_signal(frequencies):
    global Fs
    t = np.arange(0, 320 / Fs, 1 / Fs)  # Updated time vector range

    low_freq_signal = np.cos(2 * np.pi * frequencies[0] * t)
    mid_freq_signal = np.cos(2 * np.pi * frequencies[1] * t)
    high_freq_signal = np.cos(2 * np.pi * frequencies[2] * t)

    # Combine the three frequency components using the given equation
    signal = low_freq_signal + mid_freq_signal + high_freq_signal

    # Normalize the signal to ensure values are within the valid range
    signal /= np.max(np.abs(signal))

    # Scale the signal to 16-bit integer range
    signal *= 32767
    signal = signal.astype(np.int16)

    return signal

def play_audio(encoded_signal):
    try:
        sa.play_buffer(encoded_signal, num_channels=1, bytes_per_sample=2, sample_rate=Fs)
    except sa.error as e:
        print(f"Error in play_audio: {e}")

def save_audio(encoded_signal, filename):
    try:
        with wave.open(filename, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(Fs)
            wf.writeframes(encoded_signal.tobytes())
        print(f"Audio saved as {filename}")
    except Exception as e:
        print(f"Error in save_audio: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncoderApp(root)
    root.mainloop()
