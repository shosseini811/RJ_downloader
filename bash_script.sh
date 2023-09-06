#!/bin/bash

# If requirements.txt changed, then install new requirements
if [ "$REQ_CHANGED" -eq "1" ]; then
    pip install -r ~/requirements.txt
fi

# Kill the currently running Radio Javan Downloader script
pkill -f rj_downloader.py

# Start the updated script
nohup python3 ~/rj_downloader.py > /dev/null 2>&1 < /dev/null &

# Exit gracefully
exit 0
