# javis.py
import os
import wave
import datetime
import pyaudio

# --- 녹음 설정 ---
CHUNK = 1024        # 버퍼 크기
FORMAT = pyaudio.paInt16  # 16비트 음성
CHANNELS = 1        # 모노
RATE = 44100        # 샘플레이트 (44.1kHz)
RECORD_SECONDS = 5  # 녹음 시간 (초 단위)

def record_voice():
    # records 폴더 생성
    save_dir = os.path.join(os.getcwd(), "records")
    os.makedirs(save_dir, exist_ok=True)

    # 현재 날짜시간 기반 파일명 생성
    now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{now}.wav"
    filepath = os.path.join(save_dir, filename)

    # PyAudio 객체 생성
    audio = pyaudio.PyAudio()

    # 마이크 스트림 열기
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("🎙️ 녹음을 시작합니다...")

    frames = []

    # 지정된 시간만큼 녹음
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("✅ 녹음이 완료되었습니다.")

    # 스트림 종료
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # wav 파일로 저장
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"💾 파일이 저장되었습니다: {filepath}")

if __name__ == "__main__":
    record_voice()
