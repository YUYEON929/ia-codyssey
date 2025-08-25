# caesar_hacking.py
import string

def caesar_cipher_decode(target_text: str):
    alphabet = string.ascii_lowercase
    results = []

    print("\n🔎 Trying all possible Caesar cipher shifts...\n")
    for shift in range(len(alphabet)):
        decoded = ""
        for ch in target_text:
            if ch.isalpha():
                is_upper = ch.isupper()
                idx = alphabet.index(ch.lower())
                new_idx = (idx - shift) % len(alphabet)
                new_char = alphabet[new_idx]
                decoded += new_char.upper() if is_upper else new_char
            else:
                decoded += ch
        print(f"[Shift {shift}] {decoded}")
        results.append((shift, decoded))

    return results


if __name__ == "__main__":
    # 1. password.txt 읽기
    with open("password.txt", "r") as f:
        target_text = f.read().strip()

    print(f"\n🔐 Loaded text from password.txt: {target_text}\n")

    # 2. 해독 시도
    results = caesar_cipher_decode(target_text)

    # 3. 사용자가 맞는 shift 선택
    try:
        shift_num = int(input("\n👉 정답으로 보이는 Shift 번호를 입력하세요: "))
        decoded_text = results[shift_num][1]

        # 4. result.txt 저장
        with open("result.txt", "w") as f:
            f.write(decoded_text)

        print(f"\n✅ Shift {shift_num} 결과를 result.txt에 저장했습니다.")
    except (ValueError, IndexError):
        print("⚠️ 올바른 번호를 입력하지 않았습니다.")
