class SysUtils:
    def find_large_files(self, root_dir: str):
        import os
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    size = os.path.getsize(filepath) / (1024 * 1024)
                    if size > 100:
                        print(f"{filepath} - {size:.1f} MB")
                except OSError as e:
                    print(f"Error accessing {filepath}: {e}")

    def extract_errors(self, log_path: str, output_path: str):
        import re
        with open(log_path, 'r') as log_file, open(output_path, 'w') as output_file:
            for line in log_file:
                if re.search(r'\bERROR\b', line):
                    output_file.write(line)

    def safe_divide(self):
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

    def check_disk_usage(self):
        import subprocess
        try:
            result = subprocess.run(['df', '-h'], capture_output=True, text=True)
            lines = result.stdout.splitlines()
            for line in lines[1:]:
                parts = line.split()
                if len(parts) > 4:
                    usage = parts[4]
                    if usage.endswith('%') and int(usage[:-1]) > 90:
                        print(f"Warning: {parts[0]} is at {usage} usage!")
        except subprocess.CalledProcessError as e:
            print(f"Error running 'df -h': {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def _ping_host(host):
        import subprocess
        try:
            result = subprocess.run(['ping', '-c', '1', host], capture_output=True, text=True)
            if result.returncode == 0:
                return f"{host} is reachable"
            else:
                return f"{host} is not reachable"
        except subprocess.CalledProcessError as e:
            return f"Error pinging {host}: {e}"

    def ping_server(self, hosts=None):
        from concurrent.futures import ProcessPoolExecutor
        if hosts is None:
            hosts = ['8.8.8.8', '8.8.4.4', '1.1.1.1']
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(SysUtils._ping_host, hosts))
        for res in results:
            print(res)

    def mask_passwords(self, file_path: str, new_file: str):
        import re
        with open(file_path, 'r') as file:
            content = file.read()
        masked_content = re.sub(r'(?<=password=).*', '********', content)
        with open(new_file, 'w') as file:
            file.write(masked_content)

    def extract_unique_words(self, sentences: list[str]) -> list[str]:
        import re
        unique_words = set()
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            unique_words.update(words)
        return sorted(unique_words)

    def get_public_ip(self):
        import requests
        try:
            response = requests.get("https://api.ipify.org?format=json")
            response.raise_for_status()
            data = response.json()
            print(f"Your IP is: {data['ip']}")
        except requests.RequestException as e:
            print(f"Error fetching public IP: {e}")

    def is_port_open(self, host: str, port: int) -> bool:
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

    def find_sum_pairs(self, nums: list[int], target: int) -> list[tuple[int, int]]:
        seen = set()
        pairs = set()
        for num in nums:
            complement = target - num
            if complement in seen:
                pairs.add((min(num, complement), max(num, complement)))
            seen.add(num)
        print(list(pairs))

    def rolling_average(self, data: list[float], window_size: int) -> list[float]:
        if window_size <= 0:
            return []
        if window_size > len(data):
            return [sum(data) / len(data)] if data else []
        averages = []
        for i in range(len(data) - window_size + 1):
            window = data[i:i + window_size]
            averages.append(sum(window) / window_size)
        print(averages)

    def detect_spikes(self, metrics: list[float]) -> list[float]:
        if not metrics:
            return []
        average = sum(metrics) / len(metrics)
        spikes = [value for value in metrics if value > 2 * average]
        print(spikes)

    def most_common_code(self, codes: list[str]) -> str:
        from collections import Counter
        if not codes:
            return None
        code_counts = Counter(codes)
        most_common = code_counts.most_common(1)
        print(most_common[0][0] if most_common else None)

    def merge_unique_ips(self, *ip_lists: list[str]) -> list[str]:
        unique_ips = set()
        for ip_list in ip_lists:
            unique_ips.update(ip_list)
        print(sorted(unique_ips))


def main():
    utils = SysUtils()
    print("Finding large files:")
    utils.find_large_files("/Users/dshakalo/git")

    print("\nExtracting error logs:")
    utils.extract_errors("app.log", "errors_only.log")

    print("\nSafe division:")
    utils.safe_divide()

    print("\nChecking disk usage:")
    utils.check_disk_usage()

    print("\nPinging server:")
    utils.ping_server(["google.com"])

    print("\nMasking passwords:")
    utils.mask_passwords("config.ini", "config_masked.ini")

    print("\nExtracting unique words:")
    unique_words = utils.extract_unique_words(["Hello world", "world of DevOps"])
    print(unique_words)

    print("\nFetching public IP:")
    utils.get_public_ip()

    print("\nChecking open port:")
    utils.is_port_open("www.microsoft.com", 443)

    print("\nFinding sum pairs:")
    utils.find_sum_pairs([1, 2, 3, 4, 5], 5)

    print("\nCalculating rolling average:")
    utils.rolling_average([1, 2, 3, 4, 5], 3)

    print("\nDetecting spikes:")
    utils.detect_spikes([10, 12, 11, 55, 56, 13])

    print("\nFinding most common code:")
    utils.most_common_code(["200", "404", "500", "404", "404"])

    print("\nMerging unique IPs:")
    utils.merge_unique_ips(["192.168.1.1", "10.0.0.1"], ["10.0.0.1", "172.16.0.1"])


if __name__ == '__main__':
    main()