/**
 *
 * @file interrupts.cpp
 * @author Sasisekhar Govind
 *
 */
#include "interrupts.hpp"

// SYSC 4001 - Assignment 1
// Thomas Selwyn (101183163)
// Rayyan Kashif (102474266)

int main(int argc, char** argv) {

    //vectors is a C++ std::vector of strings that contain the address of the ISR
    //delays  is a C++ std::vector of ints that contain the delays of each device
    //the index of these elemens is the device number, starting from 0
    auto [vectors, delays] = parse_args(argc, argv);
    std::ifstream input_file(argv[1]);

    std::string trace;      //!< string to store single line of trace file
    std::string execution;  //!< string to accumulate the execution output

    /******************ADD YOUR VARIABLES HERE*************************/

    // PLAY WITH
    int context_save_time = 10;
    int isr_activity_time = 40;

    // Required
    int total_time = 0;

    /******************************************************************/

    //parse each line of the input trace file
    while(std::getline(input_file, trace)) {
        auto [activity, duration_intr] = parse_trace(trace);

        /******************ADD YOUR SIMULATION CODE HERE*************************/
        // activity = CPU/SYS CALL/ENDIO
        // duration_intr = DURATION (ms) or IO DEV#
        // vectors[DEV] returns str of ISR address

        if (activity == "CPU") {
            execution.append(std::to_string(total_time) + ", " + std::to_string(duration_intr) + ", cpu" + "\n");
            total_time += duration_intr; // Add cpu burn to time

        } else if (activity == "SYSCALL" || activity == "END_IO") {
            //execution.append("SYSCALL " + std::to_string(duration_intr));

            if (activity == "END_IO") {
                int delay_time = delays[duration_intr];
                execution += std::to_string(total_time) + ", " + std::to_string(delay_time) + ", end of I/O " + std::to_string(duration_intr) + ": interrupt\n";
                total_time += delay_time;
            }

            // intr_boilerplate does kernel/save context/find vector/load into PC
            std::pair<std::string, int> interruptAnalysis = intr_boilerplate(total_time, duration_intr, context_save_time, vectors);
            execution.append(interruptAnalysis.first); // add boilerplate output to output
            total_time = interruptAnalysis.second;

            // exec ISR body
            execution += std::to_string(total_time) + ", " + std::to_string(isr_activity_time) + ", execute interrupt service routine\n";
            total_time += isr_activity_time;

            // IRET
            execution += std::to_string(total_time) + ", " + std::to_string(1) + ", execute interrupt return\n";
            total_time += 1;

        } else {
            // UNSUPPORTED TRACE STATEMENT
            execution.append("Unsupported statement\n");
        }

        //execution.append("----------------------------------------------------------\n");

        /************************************************************************/

    }

    input_file.close();

    write_output(execution);

    return 0;
}
