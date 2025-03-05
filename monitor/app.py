import os
import re
import time
import subprocess
import threading
import datetime
from flask import Flask, render_template, jsonify, request

########################################
# Configuration & Device Information
########################################
NUM_DEVICES = 4  # How many devices to show
PING_THRESHOLD = 3  # Number of consecutive pings required to change status

# Each device now includes ping counters.
devices_info = {
    "lane-7": {"host": "aub-rfid-6@192.168.0.60", "status": False,
                "latest_folder": "", "is_recent_folder": False,
                "has_96_files": False, "fresh_and_complete": False,
                "ping_success_count": 0, "ping_fail_count": 0},
"lane-9": {"host": "aub-rfid-8@192.168.0.80", "status": False,
                "latest_folder": "", "is_recent_folder": False,
                "has_96_files": False, "fresh_and_complete": False,
                "ping_success_count": 0, "ping_fail_count": 0},
"lane-5": {"host": "aub-rfid-7@192.168.0.70", "status": False,
                "latest_folder": "", "is_recent_folder": False,
                "has_96_files": False, "fresh_and_complete": False,
                "ping_success_count": 0, "ping_fail_count": 0},
"lane-4": {"host": "aub-rfid-9@192.168.0.90", "status": False,
                "latest_folder": "", "is_recent_folder": False,
                "has_96_files": False, "fresh_and_complete": False,
                "ping_success_count": 0, "ping_fail_count": 0},
}


all_keys = list(devices_info.keys())
selected_keys = all_keys[:NUM_DEVICES]

# Base path for local folders and logs (adjust as needed)
LOCAL_BASE = "/mnt/c/Users/labau/Documents"

########################################
# Flask Setup
########################################
app = Flask(__name__)
devices_lock = threading.Lock()  # For thread-safe updates

########################################
# Helper: Ping a Device
########################################
def ping_device(ip_address):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "1", ip_address],
                                stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

########################################
# Helper: Extract Date from a String
########################################
date_pattern = re.compile(r"\bdata_(\d{4}-\d{2}-\d{2})\b")
def extract_date_from_string(s):
    match = date_pattern.search(s)
    if match:
        try:
            return datetime.datetime.strptime(match.group(1), "%Y-%m-%d").date()
        except ValueError:
            return None
    return None

########################################
# Helper: Update Folder Info for a Device
########################################
def update_folder_info(dum_id):
    info = devices_info[dum_id]
    dum_folder = os.path.join(LOCAL_BASE, dum_id)
    if os.path.exists(dum_folder):
        try:
            folders = [f for f in os.listdir(dum_folder)
                       if os.path.isdir(os.path.join(dum_folder, f))]
            if folders:
                latest_folder = max(folders,
                                    key=lambda x: os.path.getmtime(os.path.join(dum_folder, x)))
                info["latest_folder"] = latest_folder

                folder_date = extract_date_from_string(latest_folder)
                if folder_date:
                    now = datetime.date.today()
                    delta = now - folder_date
                    info["is_recent_folder"] = (delta.days <= 1)
                else:
                    info["is_recent_folder"] = False

                full_folder_path = os.path.join(dum_folder, latest_folder)
                if os.path.isdir(full_folder_path):
                    file_count = len([name for name in os.listdir(full_folder_path)
                                      if os.path.isfile(os.path.join(full_folder_path, name))])
                    info["has_96_files"] = (file_count == 96)
                else:
                    info["has_96_files"] = False

                info["fresh_and_complete"] = info["is_recent_folder"] and info["has_96_files"]
            else:
                info["latest_folder"] = ""
                info["is_recent_folder"] = False
                info["has_96_files"] = False
                info["fresh_and_complete"] = False
        except Exception as e:
            info["latest_folder"] = f"Error: {e}"
            info["is_recent_folder"] = False
            info["has_96_files"] = False
            info["fresh_and_complete"] = False
    else:
        info["latest_folder"] = ""
        info["is_recent_folder"] = False
        info["has_96_files"] = False
        info["fresh_and_complete"] = False

########################################
# Helper: Retrieve Files for a Device via rsync
########################################
def retrieve_files_for_device(dum_name, host):
    log_path = os.path.join(LOCAL_BASE, "retrieval.log")
    remote_user = host.split("@")[0]
    remote_folder = f"/home/{remote_user}/data/"
    local_dest = os.path.join(LOCAL_BASE, dum_name)
    os.makedirs(local_dest, exist_ok=True)
    with open(log_path, "a") as log_file:
        log_file.write(f"{time.ctime()}: Starting retrieval for {dum_name} from {host}\n")
    cmd = ["rsync", "-avzr", f"{host}:{remote_folder}", local_dest]
    result = subprocess.run(cmd, capture_output=True, text=True)
    with open(log_path, "a") as log_file:
        if result.returncode == 0:
            log_file.write(f"{time.ctime()}: SUCCESS retrieving {dum_name} from {host}\n")
        else:
            log_file.write(f"{time.ctime()}: FAIL retrieving {dum_name} from {host}\n")
            log_file.write(f"Command: {' '.join(cmd)}\n")
            log_file.write(f"Stdout: {result.stdout}\nStderr: {result.stderr}\n")
    with devices_lock:
        update_folder_info(dum_name)

########################################
# Helper: Get WiFi Status (using PowerShell via WSL)
########################################
def get_wifi_status():
    """
    Uses wslpath to convert the WSL path of the PowerShell script to a Windows path,
    then calls Windows PowerShell to run the script.
    Returns the output (even if the script returns a non-zero exit code).
    """
    try:
        windows_path = subprocess.check_output(
            ["wslpath", "-w", "/mnt/c/Users/labau/Documents/test/check_wifi.ps1"],
            text=True
        ).strip()
        result = subprocess.run(
            ["/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
             "-File", windows_path],
            text=True,
            capture_output=True,
            check=False
        )
        return result.stdout.strip()
    except Exception as e:
        return "Error checking WiFi: " + str(e)

########################################
# Flask Route: WiFi Status
########################################
@app.route("/wifi_status")
def wifi_status():
    status = get_wifi_status()
    return jsonify({"wifi_status": status})

########################################
# Thread: Fast Pinging Loop for Online/Offline Status (with smoothing)
########################################
def ping_loop():
    while True:
        for dum_id in selected_keys:
            host_str = devices_info[dum_id]["host"]
            ip_address = host_str.split("@")[-1]
            is_up = ping_device(ip_address)
            with devices_lock:
                if is_up:
                    devices_info[dum_id]["ping_success_count"] += 1
                    devices_info[dum_id]["ping_fail_count"] = 0
                    if devices_info[dum_id]["ping_success_count"] >= PING_THRESHOLD:
                        devices_info[dum_id]["status"] = True
                else:
                    devices_info[dum_id]["ping_fail_count"] += 1
                    devices_info[dum_id]["ping_success_count"] = 0
                    if devices_info[dum_id]["ping_fail_count"] >= PING_THRESHOLD:
                        devices_info[dum_id]["status"] = False
        time.sleep(1)

########################################
# Start Background Thread for Pinging
########################################
threading.Thread(target=ping_loop, daemon=True).start()

########################################
# Flask Routes for Device Actions
########################################
@app.route("/")
def index():
    with devices_lock:
        sliced_devices = {k: devices_info[k] for k in selected_keys}
    return render_template("index.html", devices=sliced_devices)

@app.route("/devices_status")
def devices_status():
    with devices_lock:
        sliced_devices = {k: devices_info[k] for k in selected_keys}
    return jsonify(sliced_devices)

@app.route("/download_latest", methods=["POST"])
def download_latest():
    for dum_id in selected_keys:
        with devices_lock:
            info = devices_info[dum_id]
            online = info["status"]
        if online:
            threading.Thread(target=retrieve_files_for_device,
                             args=(dum_id, info["host"]),
                             daemon=True).start()
    return jsonify({"success": True, "message": "File retrieval triggered for online devices."})

@app.route("/cleanup_old_folders", methods=["POST"])
def cleanup_old_folders():
    results = {}
    threads = []
    result_lock = threading.Lock()
    
    def cleanup_worker(dum_id):
        with devices_lock:
            info = devices_info[dum_id]
        if info["status"]:
            success, err_msg = cleanup_old_folders_on_device(info["host"])
            with result_lock:
                if not success:
                    results[dum_id] = {"success": False, "error": "Remote cleanup failed: " + err_msg}
                else:
                    results[dum_id] = {"success": True, "error": ""}
        else:
            with result_lock:
                results[dum_id] = {"success": False, "error": "Device offline, skipped cleanup."}
    
    for dum_id in selected_keys:
        t = threading.Thread(target=cleanup_worker, args=(dum_id,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    overall_success = all(res["success"] for res in results.values())
    return jsonify({"results": results, "overall_success": overall_success})

########################################
# Helper: Cleanup Old Folders on a Remote Device via SSH
########################################
def cleanup_old_folders_on_device(host):
    remote_user = host.split("@")[0]
    remote_path = f"/home/{remote_user}/data"
    cleanup_cmd = (
        f"ssh {host} 'find {remote_path} -mindepth 1 -maxdepth 1 -type d -mtime +4 -exec rm -rf {{}} \\;'"
    )
    try:
        result = subprocess.run(cleanup_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            app.logger.warning(f"Cleanup failed on {host}: {result.stderr}")
            return False, result.stderr
        return True, ""
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
