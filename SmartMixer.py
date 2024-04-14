import sys
import numpy as np
import sounddevice as sd
import soundfile as sf
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import tensorflow as tf
from essentia.standard import MonoLoader

class AudioTrack:
    def __init__(self, filename):
        if filename:
            self.data, self.sample_rate = sf.read(filename, dtype='float32')
            if len(self.data.shape) == 2:
                self.data = np.mean(self.data, axis=1)  # Convert to mono if stereo
        else:
            self.data = np.array([], dtype='float32')
            self.sample_rate = None
        self.instrument = None

def normalize_audio(track):
    max_amplitude = np.max(np.abs(track.data))
    if max_amplitude == 0:
        return track
    unity_gain = 1.0 / max_amplitude
    normalized_data = track.data * unity_gain
    normalized_track = AudioTrack('')
    normalized_track.data = normalized_data
    normalized_track.sample_rate = track.sample_rate
    normalized_track.instrument = track.instrument
    return normalized_track

class AudioPlayer(QObject):
    mix_changed = pyqtSignal(np.ndarray)
    position_changed = pyqtSignal(float)

    def __init__(self, mix, sample_rate, position_callback):
        super().__init__()
        self.buffer_size = 1024
        self.stream = sd.OutputStream(samplerate=sample_rate, channels=1, callback=self.audio_callback, blocksize=self.buffer_size)
        self.mix = mix
        self.sample_rate = sample_rate
        self.position = 0
        self.lock = threading.Lock()
        self.mix_changed.connect(self.update_mix)
        self.position_changed.connect(position_callback)
        self.is_playing = False
        self.stream.start()

    def audio_callback(self, outdata, frames, time, status):
        with self.lock:
            if status:
                print(status)
            if self.is_playing:
                chunksize = min(len(self.mix) - self.position, frames)
                outdata[:chunksize] = self.mix[self.position:self.position + chunksize, np.newaxis]
                self.position += chunksize
                if chunksize < frames:
                    outdata[chunksize:] = 0
                    raise sd.CallbackStop
                self.position_changed.emit(self.position / self.sample_rate)

    def update_mix(self, new_mix):
        with self.lock:
            self.mix = new_mix

    def play(self):
        self.is_playing = True

    def stop(self):
        self.is_playing = False
        self.stream.stop()
        self.stream.close()
        self.stream.abort()

class MainWindow(QMainWindow):
    def __init__(self, track_names):
        super().__init__()
        self.setWindowTitle("Studio Mixer with Live Waveform and Volume Controls")
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.tracks = []
        self.sample_rate = None
        self.track_sliders = []
        self.track_progress_bars = []
        self.audio_player = None
        self.track_names = track_names
        self.initializeAudioTracks()
        self.setupWaveform()
        self.addVolumeControls()
        self.addPlaybackControls()

    def initializeAudioTracks(self):
        path_prefix = "AudioFiles/"
        for name in self.track_names:
            filepath = f"{path_prefix}{name}"
            track = AudioTrack(filepath)
            normalized_track = normalize_audio(track)
            track.instrument = self.get_instrument_name(filepath)
            self.tracks.append(normalized_track)
            if self.sample_rate is None:
                self.sample_rate = normalized_track.sample_rate
        self.mix = np.sum([track.data for track in self.tracks], axis=0) / len(self.tracks)

    def get_instrument_name(self, filename):
        try:
            # Load audio
            audio = MonoLoader(filename=filename, sampleRate=16000, resampleQuality=4)()

            # Assuming 'discogs-effnet-bs64-1.pb' and 'nsynth_instrument-discogs-effnet-1.pb' are TensorFlow SavedModel directories
            embedding_model = tf.saved_model.load("path_to_discogs-effnet-bs64-1")
            embeddings = embedding_model.signatures['serving_default'](tf.constant(audio, dtype=tf.float32))[
                'PartitionedCall:1']

            classification_model = tf.saved_model.load("path_to_nsynth_instrument-discogs-effnet-1")
            predictions = classification_model.signatures['serving_default'](embeddings)['model/Softmax']

            instrument_classes = ["mallet", "string", "reed", "guitar", "synth_lead", "vocal", "bass", "flute",
                                  "keyboard", "brass", "organ"]
            predicted_instrument = instrument_classes[np.argmax(predictions)]
            return predicted_instrument
        except Exception as e:
            print(f"Error processing the file {filename}: {e}")
            return "Unknown"

    def setupWaveform(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.line_plot, = self.ax.plot([], [], 'b')
        self.update_waveform()
        self.layout.addWidget(self.canvas)

    def update_waveform(self):
        if self.mix.size > 0:
            time = np.linspace(0, len(self.mix) / self.sample_rate, num=len(self.mix))
            self.line_plot.set_data(time, self.mix)
            self.ax.set_xlim(left=0, right=time[-1])
            self.ax.set_ylim(bottom=np.min(self.mix), top=np.max(self.mix))
            self.canvas.draw()

    def addVolumeControls(self):
        volumeLayout = QHBoxLayout()
        for track_index, track in enumerate(self.tracks):
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(-200)
            slider.setMaximum(100)
            slider.setValue(0)
            slider.setTickInterval(50)
            slider.setTickPosition(QSlider.TicksBothSides)
            slider.sliderMoved.connect(lambda value, idx=track_index: self.adjust_volume(idx, value))
            self.track_sliders.append(slider)
            volumeLayout.addWidget(slider)
            progress_bar = QProgressBar()
            progress_bar.setOrientation(Qt.Vertical)
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(100)
            self.track_progress_bars.append(progress_bar)
            volumeLayout.addWidget(progress_bar)
            instrument_label = QLabel()
            instrument_label.setAlignment(Qt.AlignCenter)
            instrument_label.setStyleSheet("font-size: 8pt")
            instrument_label.setText(track.instrument)
            volumeLayout.addWidget(instrument_label)
        self.layout.addLayout(volumeLayout)

    def adjust_volume(self, track_index, value):
        with threading.Lock():
            db_value = -20 + value * (30 / 300)
            gain_multiplier = 10 ** (db_value / 20)
            prev_gain_multiplier = getattr(self.track_sliders[track_index], 'lastValue', 1)
            self.tracks[track_index].data /= prev_gain_multiplier
            self.tracks[track_index].data *= gain_multiplier
            self.track_sliders[track_index].lastValue = gain_multiplier
            new_mix = np.sum([track.data for track in self.tracks], axis=0) / len(self.tracks)
            rms_amplitude = np.sqrt(np.mean(self.tracks[track_index].data ** 2))
            self.track_progress_bars[track_index].setValue(int(rms_amplitude * 1000))
            format_string = f"<font size='2'>{db_value:.1f} dB</font>"
            self.track_progress_bars[track_index].setFormat(format_string)
            if self.audio_player:
                self.audio_player.mix_changed.emit(new_mix)
            self.mix = new_mix

    def addPlaybackControls(self):
        controlsLayout = QHBoxLayout()
        playButton = QPushButton("Play")
        stopButton = QPushButton("Stop")
        playButton.clicked.connect(self.playAudio)
        stopButton.clicked.connect(self.stopAudio)
        controlsLayout.addWidget(playButton)
        controlsLayout.addWidget(stopButton)
        self.layout.addLayout(controlsLayout)

    def playAudio(self):
        if self.audio_player:
            self.audio_player.stop()
        self.audio_player = AudioPlayer(self.mix.astype(np.float32), self.sample_rate, self.update_position_slider)
        self.audio_player.play()

    def stopAudio(self):
        if self.audio_player:
            self.audio_player.stop()

    def update_position_slider(self, position):
        pass  # Placeholder method, no need to check for position_slider stuff

if __name__ == "__main__":
    track_names = ["07_Overheads.wav", "10_BassDI.wav", "11_ElecGtr1.wav", "16_Hammond.wav", "17_LeadVox.wav"]
    app = QApplication(sys.argv)
    window = MainWindow(track_names)
    window.show()
    sys.exit(app.exec_())
