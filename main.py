import scapy.all as scapy
import datetime as dt
import time as t
import argparse
from file_management import load_inventory, update_inventory, save_inventory, set_mac_name
from config import default_subnet, arp_request_timeout, run_continous, default_interval

def get_addresses(subnet, timeout): # Returns a dict of MAC addresses (MAC : IP)
    addresses = {}
    packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=subnet)
    answered, unanswered = scapy.srp(packet, timeout=timeout, verbose=False)

    for sent, received in answered:
        addresses[received.hwsrc] = received.psrc
    return addresses

def scan(subnet=default_subnet, timeout=arp_request_timeout):
    updated_inventory, updates = update_inventory(load_inventory(), scan_result=get_addresses(subnet, timeout))
    save_inventory(updated_inventory=updated_inventory)
    if updates:
        for update in updates:
            timestamp = dt.datetime.fromisoformat(updated_inventory[update]["Last seen"]).strftime("%H:%M:%S")
            name = f"{updated_inventory[update].get("Name")} ({update})" if updated_inventory[update].get("Name") else update
            if updates[update] == "changed":
                print(f"[{timestamp}] {name} has changed its IP from {updated_inventory[update]["IPs"][-2]} to {updated_inventory[update]["IPs"][-1]}")
            elif updates[update] == "new":
                print(f"[{timestamp}] New device found: {name}")
    else:
        print(f"[{dt.datetime.now().strftime("%H:%M:%S")}] Ran scan. No new updates")

parser = argparse.ArgumentParser()
parser.add_argument("--subnet", type=str)
parser.add_argument("--interval", type=int)
parser.add_argument("--timeout", type=int)
parser.add_argument("--rename", type=str, nargs=2, action="append")
args = parser.parse_args()

if args.rename is not None:
    if args.subnet is not None:
        print("--subnet cannot be used with --rename")
        quit(1)
    elif args.interval is not None: # Should I use if or elif in these??
        print("--interval cannot be used with --rename")
        quit(1)
    elif args.timeout is not None:
        print("--timeout cannot be used with --rename")
        quit(1)

    save_inventory(set_mac_name(load_inventory(), args.rename))
    for mac, name in args.rename:
        print(f"Successfully set custom name \"{name}\" for {mac}")
    quit(0)



if args.interval is not None and args.interval < 0:
    parser.error("--interval must be nonnegative")
if args.timeout is not None and args.timeout <= 0:
    parser.error("--timeout must be positive")

subnet = args.subnet if args.subnet is not None else default_subnet
default_interval = args.interval if args.interval is not None else default_interval
timeout = args.timeout if args.timeout is not None else arp_request_timeout

while True:
    scan(subnet, timeout)

    if not run_continous:
        break

    t.sleep(default_interval)

