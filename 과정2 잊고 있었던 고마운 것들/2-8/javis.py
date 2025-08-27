# javis.py
import os
import wave
import datetime
import pyaudio
import speech_recognition as sr
import csv

# --- 녹음 설정 ---
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

def record_voice():
    """마이크에서 음성을 녹음하고 records 폴더에 wav 파일로 저장"""
    save_dir = os.path.join(os.getcwd(), "records")
    os.makedirs(save_dir, exist_ok=True)

    now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{now}.wav"
    filepath = os.path.join(save_dir, filename)

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("🎙️ 녹음을 시작합니다...")

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("✅ 녹음이 완료되었습니다.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"💾 파일이 저장되었습니다: {filepath}")
    return filepath

def list_recordings():
    """records 폴더 내 녹음된 파일 목록 가져오기"""
    save_dir = os.path.join(os.getcwd(), "records")
    if not os.path.exists(save_dir):
        print("⚠️ records 폴더가 존재하지 않습니다.")
        return []

    files = [f for f in os.listdir(save_dir) if f.endswith(".wav")]
    return [os.path.join(save_dir, f) for f in files]

def stt_and_save(wav_file):
    """음성파일을 STT로 변환 후 CSV로 저장"""
    recognizer = sr.Recognizer()

    # CSV 저장 경로 생성
    base_name = os.path.splitext(os.path.basename(wav_file))[0]
    csv_file = os.path.join(os.path.dirname(wav_file), f"{base_name}.csv")

    try:
        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)  # 전체 파일 읽기
            text = recognizer.recognize_google(audio_data, language="ko-KR")  # 한국어 인식
            print(f"🎧 {wav_file} → 인식된 텍스트: {text}")

            # CSV 저장
            with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["시간", "인식된 텍스트"])
                writer.writerow(["0:00", text])

            print(f"💾 CSV 저장 완료: {csv_file}")
    except sr.UnknownValueError:
        print(f"❌ 인식 실패: {wav_file}")
    except sr.RequestError as e:
        print(f"⚠️ 구글 API 오류: {e}")

if __name__ == "__main__":
    # 1. 녹음하기
    new_file = record_voice()

    # 2. 녹음된 파일 목록 불러오기
    recordings = list_recordings()
    print("📂 녹음된 파일 목록:", recordings)

    # 3. STT 수행 및 CSV 저장
    for rec in recordings:
        stt_and_save(rec)
