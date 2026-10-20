# LAN Device Watcher

A Python-based network discovery tool that uses ARP scanning to identify devices on a local network and track changes in their IP addresses.

## Features

- Discover devices using ARP requests.
- Detect previously unseen MAC addresses.
- Track IP address changes for known devices.
- Maintain a persistent JSON inventory.
- Record first-seen and last-seen timestamps.

## Requirements

- Python 3
- Scapy
- Network access with permissions to send ARP packets

## Usage

Install dependencies:

```bash
pip install scapy
```

Configure the target subnet in `config.py`, then run:

```bash
sudo python main.py
```

The program performs a network scans with the default interval and updates `addresses.json`.

Arguments:
- `--subnet` - Subnet to scan
- `--interval` - Interval for continuous scanning (in seconds)
- `--timeout` - Timeout for the ARP scan (in seconds)
- `--rename` - Rename or pre-register a MAC address

Examples:
```bash
sudo python main.py --subnet "192.168.69.0/27" --interval 60 --timeout 2
```
Scans subnet 192.168.69.0/27 every 60 seconds with a timeout of 2 seconds

```bash
sudo python main.py --rename "02:4A:8E:3B:11:F0" "Homelab" --rename "06:3A:8E:B4:12:F5" "PC"
```
Sets a custom name "Homelab" for the MAC address 02:4A:8E:3B:11:F0 and "PC" for 06:3A:8E:B4:12:F5. This can be used before the device is first discovered.

## Status

**Early prototype (v0.1.0)**

This project is under active development. Current functionality is limited to local ARP discovery and tracking newly detected devices and IP address changes.
