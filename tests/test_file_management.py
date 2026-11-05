from file_management import update_inventory, set_mac_name

def test_new_device():
    inventory = {}

    inventory = set_mac_name(inventory, [["AA:BB:CC:DD:EE:FF", "web server"]])

    scan_result = {"AA:BB:CC:DD:EE:FF": "192.168.1.10", "A1:B1:C1:D1:E1:F1": "192.168.1.110"}

    updated, events1 = update_inventory(inventory, scan_result)

    scan_result = {"AA:BB:CC:DD:EE:FF": "192.168.1.10", "A1:B1:C1:D1:E1:F1": "192.168.1.112"}

    updated, events2 = update_inventory(updated, scan_result)

    assert events1["AA:BB:CC:DD:EE:FF"] == "new" # Detect new IP
    assert events2["A1:B1:C1:D1:E1:F1"] == "changed" # Detect changed IP
    assert updated["AA:BB:CC:DD:EE:FF"]["Name"] == "web server" # Keep custom name when set before discovery
    assert "AA:BB:CC:DD:EE:FF" not in events2 # Same IP as before, no events for this MAC

    assert updated["A1:B1:C1:D1:E1:F1"]["Last IP"] == "192.168.1.112"

    assert updated["A1:B1:C1:D1:E1:F1"]["IPs"] == [
        "192.168.1.110",
        "192.168.1.112"
    ]
