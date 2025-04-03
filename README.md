# Simple Python DNS Server

## Description
This is a simple DNS server implemented in Python. It listens for DNS queries on UDP port 53 and resolves domain names using predefined zone files.

## Features
- Supports basic A-record (IPv4) resolution.
- Loads domain records from JSON-based zone files.
- Listens on `127.0.0.1:53` for testing purposes.
- Responds to valid DNS queries with IP addresses.

## Installation
1. Clone the repository.
2. Install Python 3.x.
3. Create a `zones/` directory with JSON-based zone files.

## Usage
Run the script:

```sh
python dns_server.py
