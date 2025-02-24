
#!/usr/bin/env python3
import re
import csv
import time
import os
import sys

def process_file(bin_filename):
    #   - Header: "aza"
    #   - Experiment digit: ([1-8])
    #   - Payload: (.*?)  
    #   - Footer: "sss"
    pattern = re.compile(r'aza([1-8])(.*?)sss', re.DOTALL)
    
    # Find all valid packets in the file
    matches = pattern.finditer(text)
    
    # Prepare CSV files and writers for each experiment (1 to 8)
    csv_files = {}
    csv_writers = {}
    for exp_num in range(1, 9):
        filename = f"experiment_{exp_num}.csv"
        try:
            # Open in append mode so new data gets added.
            # If the file is new (empty), write a header row.
            file_exists = os.path.isfile(filename) and os.stat(filename).st_size > 0
            f = open(filename, "a", newline='')
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Experiment", "Payload"])
            csv_files[exp_num] = f
            csv_writers[exp_num] = writer
        except Exception as e:
            print(f"Error opening CSV file '{filename}': {e}")
            return

    packet_count = 0
    # Process each found packet
    for match in matches:
        try:
            exp_num = int(match.group(1))
            payload = match.group(2).strip()
            # Error mitigation: skip if payload is empty.
            if not payload:
                continue
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            csv_writers[exp_num].writerow([timestamp, exp_num, payload])
            packet_count += 1
        except Exception as e:
            print(f"Error processing a packet: {e}")
            continue

    # Close all open CSV files
    for f in csv_files.values():
        f.close()

    print(f"Processed {packet_count} packets from '{bin_filename}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python GH.py <binary_file>")
    else:
        process_file(sys.argv[1])
