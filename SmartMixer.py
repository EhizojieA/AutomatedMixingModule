import sys
import sounddevice as sd
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, \
    QLabel, QMessageBox, QProgressBar
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import soundfile as sf
import threading


class AudioTrack:
    def __init__(self, filename):
        if filename:
            # Load the audio file; assuming stereo files might be present
            self.data, self.sample_rate = sf.read(filename, dtype='float32')
            if len(self.data.shape) == 2:
                self.data = np.mean(self.data, axis=1)  # Convert to mono if stereo
        else:
            self.data = np.array([], dtype='float32')
            self.sample_rate = None


def normalize_audio(track):
    # Calculate the maximum amplitude of the audio track
    max_amplitude = np.max(np.abs(track.data))

    # If the maximum amplitude is 0, return the track as is to avoid division by zero
    if max_amplitude == 0:
        return track

    # Calculate the gain multiplier required to normalize the audio to unity (0 dB)
    unity_gain = 1.0 / max_amplitude

    # Apply the gain multiplier to the audio track
    normalized_data = track.data * unity_gain

    # Create a new AudioTrack instance with the normalized data and original sample rate
    normalized_track = AudioTrack('')
    normalized_track.data = normalized_data
    normalized_track.sample_rate = track.sample_rate

    return normalized_track


class AudioPlayer(QObject):
    mix_changed = pyqtSignal(np.ndarray)
    position_changed = pyqtSignal(float)

    def __init__(self, mix, sample_rate, position_callback):
        super().__init__()
        self.buffer_size = 1024  # Increased buffer size
        self.stream = sd.OutputStream(samplerate=sample_rate, channels=1, callback=self.audio_callback,
                                      blocksize=self.buffer_size)
        self.mix = mix
        self.sample_rate = sample_rate
        self.position = 0
        self.lock = threading.Lock()  # Lock for thread safety
        self.mix_changed.connect(self.update_mix)
        self.position_changed.connect(position_callback)
        self.is_playing = False  # Track whether audio is playing or not
        self.stream.start()

    def audio_callback(self, outdata, frames, time, status):
        with self.lock:  # Ensure thread safety
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
        self.track_progress_bars = []  # List to hold progress bars for each track
        self.audio_player = None  # Placeholder for audio player instance
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
            normalized_track = normalize_audio(track)  # Normalize the audio track
            self.tracks.append(normalized_track)
            if self.sample_rate is None:
                self.sample_rate = normalized_track.sample_rate
        self.mix = np.sum([track.data for track in self.tracks], axis=0) / len(self.tracks)

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
            slider.sliderMoved.connect(
                lambda value, idx=track_index: self.adjust_volume(idx, value))  # Connect sliderMoved signal
            self.track_sliders.append(slider)
            volumeLayout.addWidget(slider)

            # Add progress bar for each track
            progress_bar = QProgressBar()
            progress_bar.setOrientation(Qt.Vertical)
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(100)
            self.track_progress_bars.append(progress_bar)
            volumeLayout.addWidget(progress_bar)

            # Add dB label for each track
            db_label = QLabel()
            db_label.setAlignment(Qt.AlignCenter)
            db_label.setStyleSheet("font-size: 8pt")  # Set font size
            db_label.setText(self.track_names[track_index])  # Set track name as label text
            volumeLayout.addWidget(db_label)
        self.layout.addLayout(volumeLayout)

    def adjust_volume(self, track_index, value):
        with threading.Lock():
            # Convert the slider value (-200 to 100) to a dB scale (-20 to 10 dB)
            db_value = -20 + value * (30 / 100)
            # Calculate the gain multiplier based on the dB scale
            gain_multiplier = 10 ** (db_value / 20)
            # Get the previous gain multiplier for the track
            prev_gain_multiplier = getattr(self.track_sliders[track_index], 'lastValue', 1)
            # Adjust the volume level for the specific track
            self.tracks[track_index].data /= prev_gain_multiplier
            self.tracks[track_index].data *= gain_multiplier
            # Store the current gain multiplier for future reference
            self.track_sliders[track_index].lastValue = gain_multiplier
            new_mix = np.sum([track.data for track in self.tracks], axis=0) / len(self.tracks)
            # Update the progress bar with the RMS amplitude of the track
            rms_amplitude = np.sqrt(np.mean(self.tracks[track_index].data ** 2))
            self.track_progress_bars[track_index].setValue(
                int(rms_amplitude * 1000))  # Scale RMS amplitude for progress bar
            # Set the format of the progress bar text to current volume level in dB
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
        self.audio_player.play()  # Start playback

    def stopAudio(self):
        if self.audio_player:
            self.audio_player.stop()

    def update_position_slider(self, position):
        pass  # Placeholder method, no need to check for position_slider


if __name__ == "__main__":
    track_names = ["07_Overheads.wav", "10_BassDI.wav", "11_ElecGtr1.wav", "16_Hammond.wav", "17_LeadVox.wav"]
    app = QApplication(sys.argv)
    window = MainWindow(track_names)
    window.show()
    sys.exit(app.exec_())
