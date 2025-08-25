# door_hacking.pyc
import itertools
import string
import time
import zipfile

def unlock_zip(zip_filename="emergency_storage_key.zip"):
    start_time = time.time()
    charset = string.digits + string.ascii_lowercase  # 0-9 + a-z
    attempt_count = 0

    with zipfile.ZipFile(zip_filename) as zf:
        for pwd_tuple in itertools.product(charset, repeat=6):
            attempt_count += 1
            password = ''.join(pwd_tuple)

            try:
                # zipfile은 바이트 비밀번호 필요
                zf.extractall(pwd=bytes(password, 'utf-8'))
                elapsed = time.time() - start_time
                print(f"[SUCCESS] Password found: {password}")
                print(f"Attempts: {attempt_count}, Elapsed time: {elapsed:.2f} sec")

                # 성공한 비밀번호를 파일에 저장
                with open("password.txt", "w") as f:
                    f.write(password)
                return password
            except:
                if attempt_count % 100000 == 0:
                    elapsed = time.time() - start_time
                    print(f"Attempts: {attempt_count}, Elapsed time: {elapsed:.2f} sec")

    print("Password not found.")
    return None


if __name__ == "__main__":
    print("🔐 Starting brute-force attack on emergency_storage_key.zip...")
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Start time: {start_time}")
    unlock_zip()
