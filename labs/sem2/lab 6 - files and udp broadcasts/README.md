### Lucas Kalani Ross
### Submitted 5/10/24 to Mr. Sea, Adv. Topics in CS

# Setup

## Start Redis Server
In a separate terminal, run __redis-server__ command to start database server that
stores in local memory. This terminal should stay open.

## Activate Virtual Environment and Install Required Modules
Create a virtual environment (venv) if one does not already exist with __python3 -m venv <venv_name>__. Activate the venv with __source <venv_name>/bin/activate__. Once the venv is active, install any required modules with __pip install -r requirements.txt__ (__requirements.txt__ lists all dependencies, such as Flask, redis, etc.). Keep the venv running while the Flask server is active. Close the venv with __deactivate__.

# Execution

## Start Peer-to-Peer Collector
Establish connections to other machines on the LAN (same Wifi) and keep track of their
IPv4 addresses in __redis__. If a connection does not send a UDP/TCP message for more than
30 seconds, that connection becomes inactive and is erased from memory.

Run __p2p.py__ with command-line arguments:
- __b__ whether or not to broadcast UDP messages every 5 seconds
- __n__ the unique number to brodcast UDP/TCP (for verification on other endpoints)

## 3. Check connections (optional)
__conn_check.py__ will list out any active IPv4 connections from the peer-to-peer collector.
This program is only for testing purposes and should be run in its own terminal.

## 4. Run Flask server
Once a venv is active, run __app.py__ in a new terminal. A new Flask application will start, with a link to the server in the terminal (should look like "http://<your_ipv4_address>:8022/<app_route>").