import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='duration_monitor.log',  # Comment this out to log to console instead
)

def monitor_process_durations(log_file, warning_threshold=300, error_threshold=600):
    """
    Monitor process durations and log warnings/errors for long-running processes.
    
    Args:
        log_file: Path to the log file
        warning_threshold: Duration in seconds that triggers a warning (default: 300 = 5 minutes)
        error_threshold: Duration in seconds that triggers an error (default: 600 = 10 minutes)
    """
    # Dictionary to store the start time of each process
    start_times = {}
    
    # Count for statistics
    total_processes = 0
    warning_count = 0
    error_count = 0
    
    # Open the log file and read it line by line
    with open(log_file, 'r') as file:
        for line in file:
            # Split each line by comma to separate the different fields
            parts = line.strip().split(',')

            # Extract the relevant information from each part
            timestamp_str = parts[0]       # Time in format HH:MM:SS
            job_info = parts[1].strip()    # Contains job type and job ID
            status = parts[2].strip()      # Either "START" or "END"
            process_id = parts[3].strip()  # The process ID (PID)
            
            # Parse the timestamp string into a datetime object
            timestamp = datetime.strptime(timestamp_str, "%H:%M:%S")
            
            # If this line shows a process starting, save its start time
            if status == "START":
                start_times[process_id] = (timestamp, job_info)
                
            # If this line shows a process ending, calculate how long it ran
            elif status == "END" and process_id in start_times:
                start_timestamp, job_info = start_times[process_id]
                duration = (timestamp - start_timestamp).total_seconds()
                total_processes += 1
                
                # Check if the duration exceeds thresholds and log appropriately
                if duration >= error_threshold:
                    log_msg = f"ERROR: Process {process_id} ({job_info}) took {duration:.1f} seconds to complete"
                    logging.error(log_msg)
                    print(log_msg)
                    error_count += 1
                elif duration >= warning_threshold:
                    log_msg = f"WARNING: Process {process_id} ({job_info}) took {duration:.1f} seconds to complete"
                    logging.warning(log_msg)
                    print(log_msg)
                    warning_count += 1
                
                # Remove from start_times to free up memory
                del start_times[process_id]
    
    # Log summary
    summary = f"Processed {total_processes} jobs: {warning_count} warnings, {error_count} errors"
    logging.info(summary)
    print(f"\n{summary}")
    
    # Check for processes that started but never ended
    if start_times:
        unfinished = f"WARNING: {len(start_times)} processes started but never ended"
        logging.warning(unfinished)
        print(unfinished)

# This is where the program starts running when executed directly
if __name__ == "__main__":
    import sys
    
    # Get the log file name from command line argument, or use "logs.log" as default
    log_file = sys.argv[1] if len(sys.argv) > 1 else "logs.log"
    
    # Define thresholds in seconds (5 minutes and 10 minutes)
    WARNING_THRESHOLD = 300
    ERROR_THRESHOLD = 600
    
    # Monitor process durations with specified thresholds
    monitor_process_durations(log_file, WARNING_THRESHOLD, ERROR_THRESHOLD)