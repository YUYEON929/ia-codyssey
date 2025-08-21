import sys
import wave
import pyaudio
import datetime
import speech_recognition as sr
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QTextEdit, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal, Qt

# --- 녹음 관련 설정 ---
CHUNK = 1024                # 한 번에 읽어들일 오디오 데이터의 크기
FORMAT = pyaudio.paInt16    # 16비트 오디오 포맷
CHANNELS = 1                # 모노 채널 
RATE = 44100                # 샘플링 속도 (Hz)
TEMP_WAV_FILE = "temp_recording.wav" # 임시 저장될 WAV 파일 이름

# === 녹음 작업을 처리할 별도의 스레드 클래스 ===
class RecorderThread(QThread):
    # 스레드 작업 완료 시 보낼 신호 정의
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def run(self):
        """스레드가 시작되면 이 메소드가 실행됨"""
        self.is_recording = True
        self.frames = []
        
        p = pyaudio.PyAudio()
        try:
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
        except OSError:
            self.error.emit("사용 가능한 마이크를 찾을 수 없습니다.\n마이크 연결을 확인해주세요.")
            p.terminate()
            return

        while self.is_recording:
            data = stream.read(CHUNK)
            self.frames.append(data)
        
        # 녹음 중지 후 정리 작업
        stream.stop_stream()
        stream.close()
        p.terminate()

        # 녹음된 데이터를 WAV 파일로 저장
        with wave.open(TEMP_WAV_FILE, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))
            
        self.finished.emit() # 작업 완료 신호 보내기

    def stop(self):
        """녹음 중지를 위한 메소드"""
        self.is_recording = False

# === 메인 애플리케이션 위젯 ===
class VoiceDiaryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.recorder_thread = None
        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("음성 인식 일기장 v2.0")
        self.setGeometry(300, 300, 500, 400)

        layout = QVBoxLayout()
        self.status_label = QLabel("버튼을 눌러 녹음을 시작하세요.", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.record_button = QPushButton("🎙️ 녹음 시작", self)
        self.record_button.setFixedHeight(40) # 버튼 높이 조절
        
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("이곳에 음성 인식 결과가 표시됩니다.")
        
        self.save_button = QPushButton("💾 일기 저장", self)
        self.save_button.setFixedHeight(40)

        layout.addWidget(self.status_label)
        layout.addWidget(self.record_button)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        # 시그널-슬롯 연결
        self.record_button.clicked.connect(self.toggle_recording)
        self.save_button.clicked.connect(self.save_diary)

    def toggle_recording(self):
        # recorder_thread가 실행 중인지 (녹음 중인지) 확인
        if self.recorder_thread and self.recorder_thread.isRunning():
            # 녹음 중지 로직
            self.recorder_thread.stop()
            self.status_label.setText("음성 처리 중... 잠시만 기다려주세요.")
            self.record_button.setEnabled(False) # 처리 중 버튼 비활성화
        else:
            # 녹음 시작 로직
            self.recorder_thread = RecorderThread()
            self.recorder_thread.finished.connect(self.transcribe_audio) # 녹음이 끝나면 변환 함수 호출
            self.recorder_thread.error.connect(self.show_error_message) # 에러 발생 시 메시지 박스
            self.recorder_thread.start() # 스레드 시작 -> run() 메소드 실행
            
            self.status_label.setText("녹음 중... 🎙️ (다시 누르면 중지)")
            self.record_button.setText("🛑 녹음 중지")
            self.text_edit.clear()

    def transcribe_audio(self):
        """WAV 파일을 텍스트로 변환"""
        r = sr.Recognizer()
        try:
            with sr.AudioFile(TEMP_WAV_FILE) as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data, language='ko-KR')
                self.text_edit.setText(text)
                self.status_label.setText("음성 인식이 완료되었습니다. 내용을 확인하고 저장하세요.")
        except sr.UnknownValueError:
            self.status_label.setText("음성을 인식할 수 없습니다. 다시 시도해주세요.")
            QMessageBox.warning(self, "인식 실패", "음성을 인식할 수 없습니다.\n너무 짧거나 주변 소음이 없는지 확인해주세요.")
        except sr.RequestError as e:
            self.status_label.setText("API 요청 오류가 발생했습니다.")
            QMessageBox.critical(self, "네트워크 오류", f"구글 음성 인식 서비스에 연결할 수 없습니다.\n인터넷 연결을 확인해주세요.\n\n오류: {e}")
        finally:
            # 버튼과 라벨 상태를 초기 상태로 복원
            self.record_button.setText("🎙️ 녹음 시작")
            self.record_button.setEnabled(True)

    def save_diary(self):
        """텍스트 에디터의 내용을 파일로 저장"""
        diary_text = self.text_edit.toPlainText().strip()
        if not diary_text:
            QMessageBox.warning(self, "알림", "저장할 내용이 없습니다.")
            return

        reply = QMessageBox.question(self, "일기 저장", "현재 내용을 파일로 저장하시겠습니까?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            now = datetime.datetime.now()
            filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(diary_text)
                self.status_label.setText(f"'{filename}' 파일로 일기가 저장되었습니다.")
                QMessageBox.information(self, "저장 완료", f"'{filename}' 파일로 성공적으로 저장되었습니다.")
            except Exception as e:
                QMessageBox.critical(self, "저장 실패", f"파일 저장 중 오류가 발생했습니다: {e}")

    def show_error_message(self, message):
        """스레드에서 발생한 에러를 메시지 박스로 표시"""
        QMessageBox.critical(self, "오류 발생", message)
        self.status_label.setText("오류가 발생했습니다. 다시 시도해주세요.")
        self.record_button.setText("🎙️ 녹음 시작")
        self.record_button.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VoiceDiaryApp()
    ex.show()
    sys.exit(app.exec())