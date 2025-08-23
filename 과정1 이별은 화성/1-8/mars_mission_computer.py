import time
import json
import random
import platform
import psutil


# --- DummySensor 클래스 ---
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
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }
        self.ds = DummySensor()

    def get_sensor_data(self, repeat=3):
        """5초마다 센서 데이터를 출력"""
        for i in range(repeat):
            self.ds.set_env()
            self.env_values = self.ds.get_env()
            print(json.dumps(self.env_values, indent=2))
            time.sleep(5)

    def get_mission_computer_info(self):
        """미션 컴퓨터의 시스템 정보를 JSON 형식으로 출력"""
        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "cpu_type": platform.processor(),
            "cpu_core_count": psutil.cpu_count(logical=True),
            "memory_size_GB": round(psutil.virtual_memory().total / (1024 ** 3), 2)
        }
        print("=== Mission Computer Info ===")
        print(json.dumps(info, indent=2))

    def get_mission_computer_load(self):
        """미션 컴퓨터의 부하 상태를 JSON 형식으로 출력"""
        load = {
            "cpu_usage_percent": psutil.cpu_percent(interval=1),
            "memory_usage_percent": psutil.virtual_memory().percent
        }
        print("=== Mission Computer Load ===")
        print(json.dumps(load, indent=2))


# --- 실행 부분 ---
if __name__ == "__main__":
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
