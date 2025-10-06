import os
import subprocess
import platform
from pathlib import Path

trace_files = "../input_files"
output_files = "../output_files"
executable_path = "../bin/interrupts"

context_save_time = [10, 20, 30]
isr_activity_time = [40, 70, 110, 130, 160, 200]

def main():
    print("Devils Trace Analysis")

    # Assert Linux Dominance
    # Python on Windows was being weird running the ./bin/interrupts file, so I just scraped windows support
    if platform.system() != "Linux":
        print("Linux is better.")
        exit()

    # Ensure output exists
    os.makedirs(output_files, exist_ok=True)
    if len(os.listdir(output_files)) > 0:
        print("Output folder contains execution results. Exiting.")
        exit()

    # Read through input files
    for file in os.listdir(trace_files):
        filepath = Path(trace_files).joinpath(file)

        for save_time in context_save_time:
            for isr_time in isr_activity_time:
                execute_sim(filepath, save_time, isr_time)

def execute_sim(trace_filepath: Path, save_time: int, isr_time: int):
    # Executing one simulation
    result = subprocess.run(
        [executable_path, str(trace_filepath), "../vector_table.txt", "../device_table.txt", str(save_time), str(isr_time)],
        capture_output=True)

    trace_file = trace_filepath.stem + "_" + str(save_time) + "_" + str(isr_time) + ".csv"
    sim_output = Path(output_files).joinpath(trace_file)

    try:
        os.rename("execution.txt", sim_output)
    except FileNotFoundError:
        print("Unable to find program execution file.")

    print(result)


if __name__ == "__main__":
    main()
