import threading
import multiprocessing
import time
import random
import json
import platform
import psutil
import sys

# ------------------ DummySensor ------------------
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


# ------------------ MissionComputer ------------------
class MissionComputer:
    def __init__(self, stop_event):
        self.env_values = {}
        self.ds = DummySensor()
        self.stop_event = stop_event

    def get_sensor_data(self):
        while not self.stop_event.is_set():
            self.ds.set_env()
            self.env_values = self.ds.get_env()
            print("[Sensor Data]", json.dumps(self.env_values, indent=2))
            time.sleep(5)

    def get_mission_computer_info(self):
        while not self.stop_event.is_set():
            info = {
                "OS": platform.system(),
                "OS Version": platform.version(),
                "CPU Type": platform.processor(),
                "CPU Cores": psutil.cpu_count(logical=False),
                "Memory Size (GB)": round(psutil.virtual_memory().total / (1024**3), 2)
            }
            print("[System Info]", json.dumps(info, indent=2))
            time.sleep(20)

    def get_mission_computer_load(self):
        while not self.stop_event.is_set():
            load = {
                "CPU Usage (%)": psutil.cpu_percent(interval=1),
                "Memory Usage (%)": psutil.virtual_memory().percent
            }
            print("[System Load]", json.dumps(load, indent=2))
            time.sleep(20)


# ------------------ 스레드 실행 함수 ------------------
def run_threads():
    stop_event = threading.Event()
    mc = MissionComputer(stop_event)

    t1 = threading.Thread(target=mc.get_sensor_data)
    t2 = threading.Thread(target=mc.get_mission_computer_info)
    t3 = threading.Thread(target=mc.get_mission_computer_load)

    t1.start()
    t2.start()
    t3.start()

    print("👉 Press 'q' and Enter to stop threads.")
    while True:
        if sys.stdin.readline().strip().lower() == 'q':
            stop_event.set()
            break

    t1.join()
    t2.join()
    t3.join()
    print("✅ All threads stopped.")


# ------------------ 프로세스 실행 함수 ------------------
def run_processes():
    stop_event = multiprocessing.Event()

    mc1 = MissionComputer(stop_event)
    mc2 = MissionComputer(stop_event)
    mc3 = MissionComputer(stop_event)

    p1 = multiprocessing.Process(target=mc1.get_sensor_data)
    p2 = multiprocessing.Process(target=mc2.get_mission_computer_info)
    p3 = multiprocessing.Process(target=mc3.get_mission_computer_load)

    p1.start()
    p2.start()
    p3.start()

    print("👉 Press 'q' and Enter to stop processes.")
    while True:
        if sys.stdin.readline().strip().lower() == 'q':
            stop_event.set()
            break

    p1.terminate()
    p2.terminate()
    p3.terminate()

    p1.join()
    p2.join()
    p3.join()
    print("✅ All processes stopped.")


# ------------------ 실행 ------------------
if __name__ == "__main__":
    mode = input("Choose mode (t=threads, p=processes): ").strip().lower()
    if mode == "t":
        run_threads()
    else:
        run_processes()
