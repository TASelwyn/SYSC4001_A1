import os
import subprocess

trace_files = "../input_files"
executable_path = "../bin/interrupts"

def main():
    print("Analysis")

    for file in os.listdir(trace_files):
        filepath = os.path.join(trace_files, file)
        execute_sim(15, 20, filepath)


def execute_sim(context_save_time: int, isr_activity_time: int, trace_file: str):
    # Executing one simulation
    result = subprocess.run([executable_path, "../input_files/trace_1.txt", "../vector_table.txt", "../device_table.txt", str(context_save_time), str(isr_activity_time)],
                            capture_output=True)
    print(result)


if __name__ == "__main__":
    main()