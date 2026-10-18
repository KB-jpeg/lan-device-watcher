import scapy.all as scapy
import datetime as dt
from file_management import load_inventory, update_inventory, save_inventory
from config import subnet, arp_request_timeout

def scan(): # Returns a dict of MAC addresses (MAC : IP)
    addresses = {}
    packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=subnet)
    answered, unanswered = scapy.srp(packet, timeout=arp_request_timeout, verbose=False)

    for sent, received in answered:
        addresses[received.hwsrc] = received.psrc
    return addresses

def main():
    updated_inventory, updates = update_inventory(load_inventory(), scan_result=scan())
    save_inventory(updated_inventory=updated_inventory)
    for update in updates:
        timestamp = dt.datetime.fromisoformat(updated_inventory[update]["Last seen"]).strftime("%H:%M:%S")
        if updates[update] == "changed":
            print(f"[{timestamp}] {update} has changed its IP from {updated_inventory[update]["IPs"][-2]} to {updated_inventory[update]["IPs"][-1]}")
        elif updates[update] == "new":
            print(f"[{timestamp}] New device found: {update}")

main()
