import os
import time
import subprocess
import threading
from flask import Flask, render_template, jsonify, request

########################################
#  Configure how many devices to show
########################################
NUM_DEVICES = 1  # e.g. 5 => "dum-1" ... "dum-5"

########################################
#  Device Info
########################################
# We store up to 10 devices in a dictionary:
# "dum-1": {"host": "a-1@192.168.0.61", ... }
devices_info = {
    "dum-1": {"host": "aub-rfid-4@192.168.1.203", "status": False, "latest_file": ""},
    "dum-2": {"host": "aub-rfid-3@192.168.1.202", "status": False, "latest_file": ""},
}

# We'll slice the first NUM_DEVICES for display.
all_keys = list(devices_info.keys())  # ["dum-1", ..., "dum-10"]
selected_keys = all_keys[:NUM_DEVICES]

########################################
#  Paths
########################################
# 1) If you want to still have a "download latest" button
#    that retrieves ALL devices at once, keep the master script:
MASTER_SCRIPT_PATH = "/home/uday/auto_retrieve_all.sh"

# 2) Where local dum-* folders are stored
LOCAL_BASE = f"/home/uday/Documents"

########################################
#  Flask Setup
########################################
app = Flask(__name__)

########################################
#  Real-Time Ping Function
########################################
def ping_device(ip_address):
    """
    Returns True if ping succeeds, False otherwise.
    Adjust -W and -c if you want different timeouts/attempts.
    """
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "1", ip_address],
                                stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

########################################
#  Single-Device Retrieval Function
########################################
def retrieve_files_for_device(dum_name, host):
    """
    Runs rsync for a single device, using the user's 'Documents/a' path on remote.
    Writes logs to /tmp/single_device_retrieval.log
    """
    log_path = "/tmp/single_device_retrieval.log"
    remote_user = host.split("@")[0]
    remote_ip = host.split("@")[1]

    remote_folder = f"/home/{remote_user}/Documents/a/"
    local_dest = os.path.join(LOCAL_BASE, dum_name)
    
    with open(log_path, "a") as log_file:
        log_file.write(f"{time.ctime()}: Starting retrieval for {dum_name} => {host}\n")

    os.makedirs(local_dest, exist_ok=True)

    # Run rsync
    cmd = ["rsync", "-avzr", f"{host}:{remote_folder}", local_dest]
    result = subprocess.run(cmd, capture_output=True, text=True)

    with open(log_path, "a") as log_file:
        if result.returncode == 0:
            log_file.write(f"{time.ctime()}: SUCCESS retrieving {dum_name} from {host}\n")
        else:
            log_file.write(f"{time.ctime()}: FAIL retrieving {dum_name} from {host}\n")
            log_file.write(f"Command: {' '.join(cmd)}\n")
            log_file.write(f"Stdout: {result.stdout}\nStderr: {result.stderr}\n")

########################################
#  Background Thread:
#    Real-time ping + run retrieval on
#    transitions from OFFLINE -> ONLINE
########################################
old_status = {k: False for k in devices_info}  # track previous statuses

def update_devices_loop():
    while True:
        for dum_id in selected_keys:
            info = devices_info[dum_id]
            host_str = info["host"]        # e.g. "a-1@192.168.0.61"
            ip_address = host_str.split("@")[-1]  # e.g. "192.168.0.61"

            # 1) Ping check
            is_up = ping_device(ip_address)

            # 2) If device is up now, but was offline before => run retrieval
            if is_up and not old_status[dum_id]:
                retrieve_files_for_device(dum_id, host_str)

            # 3) Mark current status
            info["status"] = is_up
            old_status[dum_id] = is_up

            # 4) Check local folder for the latest file if is_up
            if is_up:
                dum_folder = os.path.join(LOCAL_BASE, dum_id)
                if os.path.exists(dum_folder):
                    try:
                        files = [
                            f for f in os.listdir(dum_folder)
                            if os.path.isfile(os.path.join(dum_folder, f))
                        ]
                        if files:
                            latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(dum_folder, x)))
                            info["latest_file"] = latest_file
                        else:
                            info["latest_file"] = ""
                    except Exception as e:
                        info["latest_file"] = f"Error: {e}"
                else:
                    info["latest_file"] = ""
            else:
                # If offline, no latest file
                info["latest_file"] = ""

        # Sleep a bit before next check
        time.sleep(5)

# Start the background thread
thread = threading.Thread(target=update_devices_loop, daemon=True)
thread.start()

########################################
#  Flask Routes
########################################

@app.route("/")
def index():
    # Slice the devices to show only NUM_DEVICES
    sliced_devices = {k: devices_info[k] for k in selected_keys}
    return render_template("index.html", devices=sliced_devices)

@app.route("/devices_status")
def devices_status():
    # Return JSON with the current slice of devices
    sliced_devices = {k: devices_info[k] for k in selected_keys}
    return jsonify(sliced_devices)

@app.route("/download_latest", methods=["POST"])
def download_latest():
    """
    Manually trigger the master script that retrieves from ALL devices (a-1..a-10).
    If you only want to retrieve the first NUM_DEVICES, you'd have to customize that script or create a new one.
    """
    try:
        subprocess.Popen([MASTER_SCRIPT_PATH])
        return jsonify({"success": True, "message": "File retrieval initiated for ALL devices."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to initiate retrieval: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
