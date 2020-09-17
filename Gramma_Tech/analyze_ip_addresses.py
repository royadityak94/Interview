import os
import re

def validate_ip_addresses(ip):
    splits  = ip.split('.')
    for split in splits:
        if not int(split) in range(256):
            return False
    return True

def extract_ip_addresses(path, file_name):
    if not os.path.exists(os.path.join(path, file_name)):
        return []
    with open(os.path.join(path, file_name), 'r') as file_ptr:
        data = file_ptr.read()
        ip_addresses = re.findall(r'\d+\.\d+\.\d+\.\d+', data) #x.x.x.x
        valid_ips = [ip for ip in ip_addresses if validate_ip_addresses(ip)]
        return valid_ips
    file_ptr.close()

def fetch_ips(path, file_name, ip_crawled):
    ip_addresses = extract_ip_addresses(os.path.join(path), file_name)
    for ip_address in ip_addresses:
        if ip_address not in ip_crawled:
            ip_crawled.add(ip_address)
    return ip_crawled

def main():
    base_path = 'test/root2/data'
    unique_ips = set()
    for dir in os.listdir(base_path):
        if os.path.isdir(os.path.join(base_path, dir)):
            for file in os.listdir(os.path.join(base_path, dir)):
                unique_ips = fetch_ips(os.path.join(base_path, dir), file, unique_ips)
        else:
            unique_ips = fetch_ips(base_path, dir, unique_ips)

    print (unique_ips)
    expected = ['0.0.0.0', '127.0.0.1', '127.0.49.1', '127.0.64.1', '127.65.64.1', '127.98.0.1', '128.128.4.11', '128.57.107.76', '128.68.4.11', '128.96.107.55', '128.99.107.55', '128.99.58.55', '15.128.4.65', '26.56.4.23', '67.128.4.11', '7.7.7.8', '74.0.65.76', '77.255.255.254']

    print ("Length of Expected and Received:", len(unique_ips), len(expected))
    for result in unique_ips:
        if result not in expected:
            print ("Not found: ", result)



main()
