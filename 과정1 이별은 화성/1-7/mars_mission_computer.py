import time
import json
import random


# --- DummySensor 클래스 (문제 3에서 만든 것) ---
class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    def get_env(self):
        return self.env_values


# --- MissionComputer 클래스 ---
class MissionComputer:
    def __init__(self):
        # 센서 데이터를 저장할 딕셔너리
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }
        # DummySensor 인스턴스 생성
        self.ds = DummySensor()

    def get_sensor_data(self):
        while True:
            # 1. 센서 값 갱신
            self.ds.set_env()
            self.env_values = self.ds.get_env()

            # 2. JSON 형태로 출력
            print(json.dumps(self.env_values, indent=2))

            # 3. 5초 대기
            time.sleep(5)


# --- 실행 부분 ---
if __name__ == "__main__":
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
