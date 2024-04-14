import sys
import numpy as np
import sounddevice as sd
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import soundfile as sf

class AudioTrack:
    def __init__(self, filename):
        self.data, self.sample_rate = sf.read(filename, dtype='float32')
        if len(self.data.shape) == 2:
            self.data = np.mean(self.data, axis=1)  # Convert to mono if stereo

class AudioPlayer:
    def __init__(self, tracks, sample_rate):
        self.tracks = tracks
        self.sample_rate = sample_rate
        self.volumes = np.ones(len(tracks))
        self.stream = sd.OutputStream(samplerate=sample_rate, channels=1, callback=self.audio_callback)
        self.stream.start()

    def audio_callback(self, outdata, frames, time, status):
        mix = np.zeros(frames)
        for track, volume in zip(self.tracks, self.volumes):
            mix += track.data[:frames] * volume
        mix = np.clip(mix, -1, 1)  # Avoid clipping issues
        outdata[:] = mix[:, np.newaxis]

    def update_volumes(self, volumes):
        self.volumes = np.array(volumes)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Studio Mixer with Live Waveform and Volume Controls")
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.initializeAudioTracks()
        self.setupWaveform()
        self.addVolumeControls()
        self.addPlaybackControls()

    def initializeAudioTracks(self):
        track_names = ["07_Overheads.wav", "10_BassDI.wav", "11_ElecGtr1.wav", "16_Hammond.wav", "17_LeadVox.wav"]
        path_prefix = "AudioFiles/"
        self.tracks = [AudioTrack(f"{path_prefix}{name}") for name in track_names]
        self.sample_rate = self.tracks[0].sample_rate

    def setupWaveform(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.line_plot, = self.ax.plot([], [], 'b')
        self.update_waveform()
        self.layout.addWidget(self.canvas)

    def update_waveform(self):
        if hasattr(self, 'audio_player'):
            mix = sum(t.data * v for t, v in zip(self.tracks, self.audio_player.volumes))
        else:
            mix = sum(t.data for t in self.tracks) / len(self.tracks)
        time = np.linspace(0, len(mix) / self.sample_rate, num=len(mix))
        self.line_plot.set_data(time, mix)
        self.ax.set_xlim(left=0, right=time[-1])
        self.ax.set_ylim(bottom=np.min(mix), top=np.max(mix))
        self.canvas.draw()

    def addVolumeControls(self):
        volumeLayout = QHBoxLayout()
        for i in range(len(self.tracks)):
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(100)
            slider.valueChanged.connect(lambda value, idx=i: self.adjust_volume(idx, value))
            volumeLayout.addWidget(slider)
            self.track_sliders.append(slider)
        self.layout.addLayout(volumeLayout)

    def adjust_volume(self, index, value):
        if hasattr(self, 'audio_player'):
            volumes = [slider.value() / 100.0 for slider in self.track_sliders]
            self.audio_player.update_volumes(volumes)
            self.update_waveform()

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
        if not hasattr(self, 'audio_player'):
            self.audio_player = AudioPlayer(self.tracks, self.sample_rate)
        self.update_waveform()

    def stopAudio(self):
        if hasattr(self, 'audio_player'):
            self.audio_player.stop()
            del self.audio_player
        self.update_waveform()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
