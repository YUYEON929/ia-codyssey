# door_hacking.py
import itertools
import string
import time
import zipfile
import os
import json

PROGRESS_FILE = "progress.json"

def save_progress(attempt_count, last_password):
    """현재 진행 상황을 progress.json에 저장"""
    data = {
        "attempt_count": attempt_count,
        "last_password": last_password
    }
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)

def load_progress():
    """진행 상황 불러오기 (없으면 None 반환)"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return None

def unlock_zip(zip_filename="emergency_storage_key.zip"):
    start_time = time.time()
    charset = string.digits + string.ascii_lowercase  # 0-9 + a-z
    attempt_count = 0
    resume_from = None

    # 이전 진행상황 불러오기
    progress = load_progress()
    if progress:
        attempt_count = progress["attempt_count"]
        resume_from = progress["last_password"]
        print(f"🔄 Resuming from attempt {attempt_count}, last password: {resume_from}")
    else:
        print("🆕 Starting fresh brute-force attack...")

    with zipfile.ZipFile(zip_filename) as zf:
        # resume_from이 있으면 그 이후부터 시작
        generator = itertools.product(charset, repeat=6)
        if resume_from:
            # resume_from 다음부터 시작하도록 건너뛰기
            skip = attempt_count
            for _ in range(skip):
                next(generator)

        for pwd_tuple in generator:
            attempt_count += 1
            password = ''.join(pwd_tuple)

            try:
                zf.extractall(pwd=bytes(password, 'utf-8'))
                elapsed = time.time() - start_time
                print(f"[SUCCESS] Password found: {password}")
                print(f"Attempts: {attempt_count}, Elapsed time: {elapsed:.2f} sec")

                with open("password.txt", "w") as f:
                    f.write(password)

                # 성공 시 진행상황 기록 삭제
                if os.path.exists(PROGRESS_FILE):
                    os.remove(PROGRESS_FILE)
                return password
            except:
                # 10만 번마다 진행상황 저장
                if attempt_count % 100000 == 0:
                    elapsed = time.time() - start_time
                    print(f"Attempts: {attempt_count}, Elapsed time: {elapsed:.2f} sec")
                    save_progress(attempt_count, password)

    print("Password not found.")
    return None


if __name__ == "__main__":
    print("🔐 Starting brute-force attack on emergency_storage_key.zip...")
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Start time: {start_time}")
    unlock_zip()
