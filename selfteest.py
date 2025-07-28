# SECTION 1: Loops, Conditionals, Functions
import subprocess
from concurrent.futures import ProcessPoolExecutor
import os
import re


def find_large_files(root_dir: str):
    '''
    Find Large Files
    Write a function that loops through a directory recursively and prints out files larger than 100MB.
    Example:
        find_large_files("/var/log")
    Expected Output:
        /var/log/huge.log - 120.5 MB
        /var/log/archive/2023.log - 250.1 MB
    '''
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                size = os.path.getsize(filepath) / (1024 * 1024)  # Convert to MB
                if size > 100:
                    print(f"{filepath} - {size:.1f} MB")
            except OSError as e:
                print(f"Error accessing {filepath}: {e}")


# SECTION 2: Reading / Writing Files

def extract_errors(log_path: str, output_path: str):
    '''
    Extract Error Logs
    Given a large log file, extract all lines containing the word "ERROR" and write them to a new file.
    Example:
        extract_errors("app.log", "errors_only.log")
    Expected Output:
        errors_only.log will contain only lines with "ERROR"
    '''
    with open(log_path, 'r') as log_file, open(output_path, 'w') as output_file:
        for line in log_file:
            if re.search(r'\bERROR\b', line):
                output_file.write(line)


# SECTION 3: Exception Handling

def safe_divide():
    '''
    Safe Division Utility
    Write a function that divides two numbers provided by the user, and gracefully handles division by zero and invalid input.
    Example:
        safe_divide() # User inputs: 10, 2
    Expected Output:
        5.0
    '''
    while True:
        try:
            num1 = float(input("Enter the numerator: "))
            num2 = float(input("Enter the denominator: "))
            result = num1 / num2
            print(f"Result: {result}")
            break
        except ZeroDivisionError:
            print("Error: Division by zero is not allowed. Please try again.")
        except ValueError:
            print("Error: Invalid input. Please enter numeric values.")


# SECTION 4: Calling Shell Commands

def check_disk_usage():
    '''
    Disk Usage Check
    Write a script that uses subprocess.run to call `df -h`, parses the output, and alerts if any partition is over 90% used.
    Example:
        check_disk_usage()
    Expected Output:
        Warning: /dev/sda1 is at 95% usage!
    '''
    try:
        result = subprocess.run(['df', '-h'], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        for line in lines[1:]:  # Skip the header
            parts = line.split()
            if len(parts) > 4:
                usage = parts[4]
                if usage.endswith('%') and int(usage[:-1]) > 90:
                    print(f"Warning: {parts[0]} is at {usage} usage!")
    except subprocess.CalledProcessError as e:
        print(f"Error running 'df -h': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def ping_host(host):
    try:
        result = subprocess.run(['ping', '-c', '1', host], capture_output=True, text=True)
        if result.returncode == 0:
            return f"{host} is reachable"
        else:
            return f"{host} is not reachable"
    except subprocess.CalledProcessError as e:
        return f"Error pinging {host}: {e}"


def ping_server(host="8.8.8.8"):
    hosts = ['8.8.8.8', '8.8.4.4', '1.1.1.1']
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(ping_host, hosts))
    for res in results:
        print(res)


# SECTION 5: String Manipulation & Regular Expressions

def mask_passwords(file_path: str, new_file: str):
    '''
    Sanitize Passwords
    Given a config file, replace any line with `password=` to mask the value as ******** using regex.
    Example:
        mask_passwords("config.ini")
    Expected Output (in-place or new file):
        password=********
    '''
    with open(file_path, 'r') as file:
        content = file.read()
    masked_content = re.sub(r'(?<=password=).*', '********', content)
    with open(new_file, 'w') as file:
        file.write(masked_content)


# SECTION 6: Array (List) Manipulations

def extract_unique_words(sentences: list[str]) -> list[str]:
    '''
    Unique Sorted Words
    Given a list of sentences, extract all unique words, lowercase them, and return a sorted list.
    Example:
        extract_unique_words(["Hello world", "world of DevOps"])
    Expected Output:
        ['devops', 'hello', 'of', 'world']
    '''
    unique_words = set()
    for sentence in sentences:
        words = re.findall(r'\b\w+\b', sentence.lower())
        unique_words.update(words)
    return sorted(unique_words)


# SECTION 7: REST API Call with Requests

def get_public_ip():
    '''
    Fetch IP Info
    Call https://api.ipify.org?format=json and print the user's public IP.
    Example:
        get_public_ip()
    Expected Output:
        Your IP is: 123.45.67.89
    '''
    import requests
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        print(f"Your IP is: {data['ip']}")
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")


# SECTION 8: Network Port Monitoring

def is_port_open(host: str, port: int) -> bool:
    '''
    Check Open Port
    Write a function to check if port 22 is open on a given host using socket.
    Example:
        is_port_open("localhost", 22)
    Expected Output:
        True (if SSH is running)
    '''
    import socket
    try:
        with socket.create_connection((host, port), timeout=5):
            print(f"Port {port} on {host} is open.")
            return True
    except (socket.timeout, ConnectionRefusedError):
        print(f"Port {port} on {host} is closed or not reachable.")
        return False
    except socket.error as e:
        print(f"Socket error: {e}")
        return False


# SECTION 10: More Sophisticated Array Manipulations

def find_sum_pairs(nums: list[int], target: int) -> list[tuple[int, int]]:
    '''
    Find Pairs with Target Sum
    Given a list of integers and a target number, return all unique pairs that sum to the target.
    Example:
        find_sum_pairs([1, 2, 3, 4, 5], 5)
    Expected Output:
        [(1, 4), (2, 3)]
    '''

    seen = set()
    pairs = set()
    for num in nums:
        complement = target - num
        if complement in seen:
            pairs.add((min(num, complement), max(num, complement)))
        seen.add(num)
    print(list(pairs))


def rolling_average(data: list[float], window_size: int) -> list[float]:
    '''
    Rolling Average Over N Entries
    Takes a list of CPU usages and returns a list of rolling averages over a window of size n.
    Example:
        rolling_average([1, 2, 3, 4, 5], 3)
    Expected Output:
        [2.0, 3.0, 4.0]
    '''
    if window_size <= 0:
        return []
    if window_size > len(data):
        return [sum(data) / len(data)] if data else []
    averages = []
    for i in range(len(data) - window_size + 1):
        window = data[i:i + window_size]
        averages.append(sum(window) / window_size)
    print(averages)



def detect_spikes(metrics: list[float]) -> list[float]:
    '''
    Detect Spike Anomalies
    Given a list of metrics, return all values that are more than 2× the average.
    Example:
        detect_spikes([10, 12, 11, 55, 13])
    Expected Output:
        [55]
    '''
    if not metrics:
        return []
    average = sum(metrics) / len(metrics)
    spikes = [value for value in metrics if value > 2 * average]
    print(spikes)


def most_common_code(codes: list[str]) -> str:
    '''
    Most Frequent Value
    Find the most frequent error code in a list of strings like: ["200", "404", "500", "404"].
    Example:
        most_common_code(["200", "404", "500", "404", "404"])
    Expected Output:
        "404"
    '''
    from collections import Counter
    if not codes:
        return None
    code_counts = Counter(codes)
    most_common = code_counts.most_common(1)
    print(most_common[0][0] if most_common else None)



def merge_unique_ips(*ip_lists: list[str]) -> list[str]:
    '''
    Merge & Deduplicate Multiple Lists
    Given multiple lists of IP addresses, merge them into one sorted list of unique IPs.
    Example:
        merge_unique_ips(["192.168.1.1", "10.0.0.1"], ["10.0.0.1", "172.16.0.1"])
    Expected Output:
        ['10.0.0.1', '172.16.0.1', '192.168.1.1']
    '''

    unique_ips = set()
    for ip_list in ip_lists:
        unique_ips.update(ip_list)
    print(sorted(unique_ips))


def main():
    print("Finding large files:")
    find_large_files("/Users/dshakalo/git")

    print("\nExtracting error logs:")
    extract_errors("app.log", "errors_only.log")

    print("\nSafe division:")
    safe_divide()

    print("\nChecking disk usage:")
    check_disk_usage()

    print("\nPinging server:")
    ping_server("google.com")

    print("\nMasking passwords:")
    mask_passwords("config.ini", "config_masked.ini")

    print("\nExtracting unique words:")
    unique_words = extract_unique_words(["Hello world", "world of DevOps"])
    print(unique_words)

    print("\nFetching public IP:")
    get_public_ip()

    print("\nChecking open port:")
    is_port_open("www.microsoft.com", 443)

    print("\nFinding sum pairs:")
    find_sum_pairs([1, 2, 3, 4, 5], 5)

    print("\nCalculating rolling average:")
    rolling_average([1, 2, 3, 4, 5], 3)
    print("\nDetecting spikes:")
    detect_spikes([10, 12, 11, 55, 56, 13])
    print("\nFinding most common code:")
    most_common_code(["200", "404", "500", "404", "404"])
    print("\nMerging unique IPs:")
    merge_unique_ips(["192.168.1.1", "10.0.0.1"], ["10.0.0.1", "172.16.0.1"])


if __name__ == '__main__':
    main()
