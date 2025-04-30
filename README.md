# Process Duration Monitor

A simple Python tool that monitors process execution times from log files.

## What it does

- Reads log files containing process start/end events
- Calculates how long each process took to run
- Warns about processes that take too long (default: >5 minutes)
- Shows errors for very long processes (default: >10 minutes)
- Detects processes that never completed

## How to use it

```bash
python duration_monitor.py [log_file]
```

If you don't specify a log file, it will use "logs.log" by default.

## Log file format

Your log files should have this format:
```
HH:MM:SS,job_type job_id,STATUS,process_id
```

Example:
```
14:25:32,BATCH JOB 12345,START,pid-78901
14:32:45,BATCH JOB 12345,END,pid-78901
```

## Output

The script will:
- Print warnings and errors to the console
- Save detailed logs to "duration_monitor.log"
- Show a summary of all processed jobs

## Requirements

- Python 3.6 or higher
- No external packages needed
