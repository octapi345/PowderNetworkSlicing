#!/bin/bash

# Path to your Python script

PYTHON_SCRIPT_PATH="/local/repository/TestScripts/mongo_test.py nfs.aseliga-173674.networkslicing.emulab.net"

# Number of iterations
N_ITERATIONS=10

# Output file for TPS results
OUTPUT_FILE="/local/repository/TestScripts/tps_results.txt"

# Clear any existing results
> $OUTPUT_FILE

# Main loop
for i in $(seq 1 $N_ITERATIONS); do
    # Capture the start time
    START_TIME=$(date +%s.%N)
    
    # Execute the Python script
    python3 $PYTHON_SCRIPT_PATH
    
    # Capture the end time
    END_TIME=$(date +%s.%N)
    
    # Calculate the duration
    DURATION=$(echo "$END_TIME - $START_TIME" | bc)
    
    # Calculate transactions per second (assuming one transaction per run for simplicity)
    TPS=$(echo "1 / $DURATION" | bc -l)
    
    # Write the TPS result to the output file
    echo "Iteration $i: $TPS transactions/second" >> $OUTPUT_FILE
done

echo "TPS results written to $OUTPUT_FILE"