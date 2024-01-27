import os
import wave
import time
import threading
import tkinter as tk
#import pyaudio
import librosa
import numpy as np

class Record:
    def __init__(incoming):
        incoming.root = tk.Tk()
        incoming.root.resizable(True, True)
        incoming.button = tk.Button(text="U+1F534")
        incoming.root.mainloop()

Record()