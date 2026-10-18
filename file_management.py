import json
import copy
import datetime as dt
from config import default_path

def load_inventory(path=default_path): # Returns dict of dicts
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        with open(path, "w") as f:
            json.dump({}, f)
        return {}


def update_inventory(inventory, scan_result): # Returns dict of dicts and detected events
    timestamp = str(dt.datetime.now().astimezone().isoformat())
    updated_inventory = copy.deepcopy(inventory)
    updates = {}
    for mac in scan_result:

        if mac in inventory: # Remembered Mac
            if inventory[mac]["Last IP"] != scan_result[mac]: # Different last IP
                updates[mac] = "changed"
                updated_inventory[mac]["Last IP"] = scan_result[mac] # Changed/New IP
                updated_inventory[mac]["IPs"].append(scan_result[mac]) # Add to IP list

        else: # New Mac
            updated_inventory[mac] = {}
            updated_inventory[mac]["Last IP"] = scan_result[mac]
            updated_inventory[mac]["IPs"] = []
            updated_inventory[mac]["IPs"].append(scan_result[mac])
            updated_inventory[mac]["First seen"] = timestamp

            updates[mac] = "new"

        updated_inventory[mac]["Last seen"] = timestamp # Update last seen
    
    return updated_inventory, updates

def save_inventory(updated_inventory, path=default_path): # Saves to file
    with open(path, "w") as f:
        json.dump(updated_inventory, f)
