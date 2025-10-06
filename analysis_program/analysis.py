import os
import subprocess
from time import sleep

trace_files = "../input_files"
executable_path = "../bin/interrupts"
default_args = "vector_table.txt device_table.txt"

def main():
    print("Analysis")

    for file in os.listdir(trace_files):
        filepath = os.path.join(trace_files, file)
        execute_sim(15, 20, filepath)
        print(file)
        sleep(50000)


def execute_sim(context_save_time: int, isr_activity_time: int, trace_file: str):
    # Executing one simulation
    result = subprocess.run([executable_path, "../input_files/trace_1.txt", default_args],
                            capture_output=True)
    print(result)

if __name__ == "__main__":
    main()