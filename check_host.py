import argparse
import json
import requests
from prettytable import PrettyTable

'''

About: This Programme Based on Check-Host API
Author: AuxGrep
Year:   2024

'''

green = "\033[92m"   
red = "\033[91m"     
reset = "\033[0m" 

net_headers = {'Accept': 'application/json'}
response_data = 'node.json'

def push_network_request(endpoint):
    try:
        response = requests.get(endpoint, headers=net_headers)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data['request_id'] 
        else:
            return 'Error'
        
    except requests.ConnectionError:
        raise ConnectionError("Connection Error occurred while making the request.")
    
def results(endpoint):
    try:
        response = requests.get(endpoint, headers=net_headers)
        if response.status_code == 200:
            data_resp = json.loads(response.text)
            with open('node.json', mode='w') as node_file:
                json.dump(data_resp, node_file)
        else:
            print("Error occurred while fetching results.")
    except requests.ConnectionRefusedError:
        print("Connection Refused by the server.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check host availability using various methods.")
    parser.add_argument("--host", help="Host to check availability for.")
    parser.add_argument("--mode", choices=['ping', 'http', 'dns', 'tcp'], help="Mode of check: ping, http, dns, or tcp.")
    try:
        args = parser.parse_args()
        if not args.host or not args.mode:
            parser.error("Both host and mode are required arguments.")
        if args.mode == 'ping':
            request_id = push_network_request(f'https://check-host.net/check-ping?host={args.host}&max_nodes=100')
            results(endpoint=f'https://check-host.net/check-result/{request_id}')
            data = {}
            with open(response_data, 'r') as file:
                data = json.load(file)
            table = PrettyTable()
            table.field_names = ["Host", "Status", "Response Time", "IP Address"]
            def process_node(node_data):
                for result in node_data:
                    status = result[0] if result else "Error"
                    response_time = result[1] if len(result) > 1 else "-"
                    ip_address = result[2] if len(result) > 2 else "-"
                    return (status, response_time, ip_address)
            for host, results in data.items():
                if results is None:
                    table.add_row([host, "No Response", "-", "-"])
                else:
                    for node_results in results:
                        status, response_time, ip_address = process_node(node_results)
                        if status == "OK":
                            status = f"\033[92m{status}\033[0m"  
                        else:
                            status = f"\033[91m{status}\033[0m"  
                        response_display = f"{response_time:.3f}s" if isinstance(response_time, float) else response_time
                        table.add_row([host, status, response_display, ip_address])
            print(table)
        elif args.mode == 'http':
            request_id = push_network_request(f'https://check-host.net/check-http?host={args.host}&max_nodes=100')
            results(endpoint=f'https://check-host.net/check-result/{request_id}')
            data = {}
            with open(response_data, 'r') as file:
                data = json.load(file)
            table = PrettyTable()
            table.field_names = ["Node", "Attempts", "Time", "Status", "Code", "Node IP"]
            colors = {
                                "Moved Permanently": "\033[93m",  
                                "OK": "\033[92m",                
                                "default": "\033[91m"            
                    }
            for node, info in data.items():
                if info:
                    attempts, time, status, code, ip = info[0]
                    if status == "Moved Permanently":
                        color = colors["Moved Permanently"]
                    elif status == "OK" or code == "200":
                        color = colors["OK"]
                    else:
                        color = colors["default"]
                    table.add_row([f"{color}{node}\033[0m", attempts, time, f"{color}{status}\033[0m", code, f"{color}{ip}\033[0m"])
            print(table)

        elif args.mode == 'dns':
            request_id = push_network_request(f'https://check-host.net/check-dns?host={args.host}&max_nodes=100')
            results(endpoint=f'https://check-host.net/check-result/{request_id}')
            with open(response_data, 'r') as file:
                data = json.load(file)
            table = PrettyTable()
            table.field_names = ["Node", "A Record", "AAAA Record", "TTL"]
            for node, records in data.items():
                if records:
                    for record in records:
                        a_record = ', '.join(record.get('A', []))
                        aaaa_record = ', '.join(record.get('AAAA', []))
                        ttl = record.get('TTL', '')
                        table.add_row([node, a_record, aaaa_record, ttl])
                else:
                    table.add_row([node, f'{red}N/A{reset}', f'{red}N/A{reset}', f'{red}N/A{reset}'])
            print(table)
                    
        elif args.mode == 'tcp':
            request_id = push_network_request(f'https://check-host.net/check-tcp?host={args.host}&max_nodes=100')
            results(endpoint=f'https://check-host.net/check-result/{request_id}')
            with open(response_data, 'r') as file:
                data = json.load(file)
            table = PrettyTable()
            table.field_names = ["Node", "IP Address", "Response Time"]
            for node, info in data.items():
                if info and isinstance(info, list) and 'address' in info[0] and 'time' in info[0]:
                    address = info[0]["address"]
                    time = f"{green}{info[0]['time']}{reset}"
                    table.add_row([node, address, time])
                else:
                    table.add_row([f"{red}{node}{reset}", f"{red}No Data{reset}", f"{red}No Data{reset}"])
            print(table)

    except argparse.ArgumentError as e:
        print(f"Argument error: {e}")
