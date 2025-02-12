#!/opt/homebrew/bin/python3

import requests
import csv

def get_user_input():
    hostname = input("Enter hostname: ")
    admin_port = input("Enter admin port: ")
    api_key = input("Enter API key: ")
    outfile = input("Enter output filename: ")
    return hostname, admin_port, api_key, outfile

def fetch_api_data(hostname, admin_port, api_key):
    url = f"https://{hostname}:{admin_port}/api/v2/monitor/switch-controller/managed-switch/status"
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_csv(data, filename):
    if "results" not in data:
        print("Invalid data format.")
        return
    
    fieldnames = ["serial", "switch-id"]
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in data["results"]:
            writer.writerow({"serial": item.get("serial", "N/A"), "switch-id": item.get("switch-id", "N/A")})
    
    print(f"Data saved to {filename}")

def main():
    hostname, admin_port, api_key, outfile = get_user_input()
    data = fetch_api_data(hostname, admin_port, api_key)
    if data:
        save_to_csv(data,outfile)

if __name__ == "__main__":
    main()

