#!/bin/bash
# Master script to rsync files from up to 10 devices.

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
LOG_FILE="/tmp/auto_retrieve_all_debug.log"

echo "$(date): Starting auto_retrieve_all.sh" >> "$LOG_FILE"

declare -A DEVICES=(
  ["dum-1"]="aub-rfid-4@192.168.1.203"
  ["dum-2"]="aub-rfid-3@192.168.1.202"  
)

REMOTE_SUBPATH="Documents/a"
LOCAL_BASE="/home/uday/Documents"  # Adjust if desired

for dum_name in "${!DEVICES[@]}"; do
    REMOTE_USER_HOST="${DEVICES[$dum_name]}"
    REMOTE_USER="${REMOTE_USER_HOST%%@*}"
    HOST="${REMOTE_USER_HOST#*@}"
    REMOTE_FOLDER="/home/$REMOTE_USER/$REMOTE_SUBPATH/"
    LOCAL_DEST="$LOCAL_BASE/$dum_name/"

    echo "$(date): Rsync from $REMOTE_USER_HOST:$REMOTE_FOLDER to $LOCAL_DEST" >> "$LOG_FILE"

    mkdir -p "$LOCAL_DEST"

    rsync -avz "$REMOTE_USER_HOST:$REMOTE_FOLDER" "$LOCAL_DEST"
    if [ $? -eq 0 ]; then
        echo "$(date): Rsync success for $REMOTE_USER_HOST" >> "$LOG_FILE"
    else
        echo "$(date): Rsync failed for $REMOTE_USER_HOST" >> "$LOG_FILE"
    fi
done
