import sys
import speedtest
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class SpeedTestThread(QThread):
    result_signal = pyqtSignal(float, float, float)

    def run(self):
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Mbps
        upload_speed = st.upload() / 1_000_000      # Mbps
        ping = st.results.ping
        self.result_signal.emit(download_speed, upload_speed, ping)

class SpeedTestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('WiFi Speed Test Tool')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.download_label = QLabel('Download Speed: N/A')
        self.upload_label = QLabel('Upload Speed: N/A')
        self.ping_label = QLabel('Ping: N/A')

        self.test_button = QPushButton('Start Speed Test')
        self.test_button.clicked.connect(self.start_speed_test)

        layout.addWidget(self.download_label)
        layout.addWidget(self.upload_label)
        layout.addWidget(self.ping_label)
        layout.addWidget(self.test_button)

        self.setLayout(layout)

    def start_speed_test(self):
        self.test_button.setEnabled(False)
        self.download_label.setText('Download Speed: Testing...')
        self.upload_label.setText('Upload Speed: Testing...')
        self.ping_label.setText('Ping: Testing...')

        self.thread = SpeedTestThread()
        self.thread.result_signal.connect(self.update_results)
        self.thread.start()

    def update_results(self, download, upload, ping):
        self.download_label.setText(f'Download Speed: {download:.2f} Mbps')
        self.upload_label.setText(f'Upload Speed: {upload:.2f} Mbps')
        self.ping_label.setText(f'Ping: {ping} ms')
        self.test_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeedTestApp()
    window.show()
    sys.exit(app.exec_())
