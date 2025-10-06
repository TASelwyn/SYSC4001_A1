import os
import subprocess
import platform
from pathlib import Path
from typing import Tuple, Any

input_files = "../input_files"
output_files = "../output_files"

context_save_time = [10, 20, 30]
isr_activity_time = [40, 70, 110, 130, 160, 200]

total_time_table_filepath = Path(output_files).joinpath("time_table.txt")

def main():
    print("Devils Trace Analysis")

    # Assert Linux Dominance
    # Python on Windows was being weird running the ./bin/interrupts file, so I just scraped windows support
    if platform.system() != "Linux":
        print("Linux is better.")
        exit()

    # Ensure output exists
    skip_run_sim = False
    os.makedirs(output_files, exist_ok=True)
    if len(os.listdir(output_files)) > 0:
        print("Output folder contains execution results. Skipping running interrupts sim program.")
        skip_run_sim = True

    # Read through input files
    if not skip_run_sim:
        for file in os.listdir(input_files):
            filepath = Path(input_files).joinpath(file)

            for save_time in context_save_time:
                for isr_time in isr_activity_time:
                    execute_sim(filepath, save_time, isr_time)

    time_table = open(str(total_time_table_filepath), "w")
    print("Analyzing trace simulation csvs to generate time table")
    # Analyse simulation traces
    for file in os.listdir(output_files):
        filepath = Path(output_files).joinpath(file)

        if filepath.stem.startswith("trace"):
            time_table.write(analyse_sim(filepath) + "\n")

    time_table.close()
    print("Generated time_table.txt from analyzed sim files.")

def execute_sim(trace_filepath: Path, save_time: int, isr_time: int):
    # Executing one simulation
    result = subprocess.run(
        ["../bin/interrupts", str(trace_filepath), "../vector_table.txt", "../device_table.txt", str(save_time),
         str(isr_time)],
        capture_output=True)

    trace_file = trace_filepath.stem + "_" + str(save_time) + "_" + str(isr_time) + ".csv"
    sim_output = Path(output_files).joinpath(trace_file)

    try:
        os.rename("execution.txt", sim_output)
    except FileNotFoundError:
        print("Unable to find program execution file.")

    print(result)


def analyse_sim(sim_path: Path) -> str:
    file = open(sim_path)

    total_execution_time = 0

    cpu_time = 0
    switch_to_kernel_time = 0
    context_switch_time = 0
    find_vector_time = 0
    load_address_time = 0
    io_delays = 0
    isr_time = 0
    return_interrupt_time = 0

    for line in file:
        split = line.split(",")
        total_time = int(split[0])
        event_duration = int(split[1])
        event_type = split[2]

        total_execution_time = total_time + event_duration

        if "cpu" in event_type:
            cpu_time += event_duration
        elif "switch to kernel mode" in event_type:
            switch_to_kernel_time += event_duration
        elif "context saved" in event_type:
            context_switch_time += event_duration
        elif "find vector" in event_type:
            find_vector_time += event_duration
        elif "load address" in event_type:
            load_address_time += event_duration
        elif "execute interrupt service routine" in event_type:
            isr_time += event_duration
        elif "execute interrupt return" in event_type:
            return_interrupt_time += event_duration
        elif "end of I/O" in event_type:
            io_delays += event_duration

    file.close()

    analysis_numbers = [sim_path.stem, total_execution_time, cpu_time, switch_to_kernel_time, context_switch_time, find_vector_time, load_address_time, isr_time, return_interrupt_time, io_delays]
    return ", ".join([str(item) for item in analysis_numbers])

if __name__ == "__main__":
    main()
