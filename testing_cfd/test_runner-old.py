import os
import time
import sys
import subprocess
from datetime import datetime

def run_tests(commands, delay, result_folder):
    # Create the results folder if it doesn't exist
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)
    
    # Create a log file with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(result_folder, f"test_results_{timestamp}.log")
    
    with open(log_file, "w") as log:
        log.write(f"Test Run Started: {datetime.now()}\n")
        log.write(f"Delay Between Runs: {delay} seconds\n")
        log.write("===========================================\n")
        
        # Run each command
        for index, command in enumerate(commands, start=1):
            log.write(f"\nTest {index}: {command}\n")
            log.write(f"Started: {datetime.now()}\n")
            try:
                # Execute the command
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                log.write("Output:\n")
                log.write(result.stdout + "\n")
                log.write("Errors:\n")
                log.write(result.stderr + "\n")
                log.write(f"Completed: {datetime.now()}\n")
            except Exception as e:
                log.write(f"Error executing command: {e}\n")
            
            # Delay before the next run
            if index < len(commands):
                time.sleep(delay)
        
        log.write("\nAll tests completed.\n")
    
    print(f"ERROR: {result.stderr}")
    print(f"Test results logged in: {log_file}")

if __name__ == "__main__":

    print("Python executable:", sys.executable)
    print("Python path:", sys.path)


    # Define the commands to run
    commands = [
        'python --version',
        'source ~/.bashrc',
        'source ~/df-env/bin/activate',
        'export LD_LIBRARY_PATH="/Users/gridharanvidi/oracle_client/instaclient-basic-macos-arm64-23.3:$LD_LIBRARY_PATH"',
        'echo $LD_LIBRARY_PATH',
        'ls -lt /Users/gridharanvidi/oracle_client/instaclient-basic-macos-arm64-23.3',
        'python send_test_mail.py "ORDER file order_ack1.pdf" test_pdf_files/order_ack1.pdf test1@test.com',
        'python send_test_mail.py "ORDER file order_ack2.pdf" test_pdf_files/order_ack2.pdf test2@test.com',
        'python send_test_mail.py "ORDER file order_ack3.pdf" test_pdf_files/order_ack3.pdf test3@test.com',
    ]

    # Set the delay in seconds between test runs
    delay = 2

    # Define the results folder
    result_folder = "test_results"

    # Run the tests
    run_tests(commands, delay, result_folder)

