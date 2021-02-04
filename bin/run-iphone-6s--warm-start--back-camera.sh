#!/bin/bash
v4l2-ctl -d /dev/video2 --set-ctrl=exposure_auto=1
python run-test.py \
    --port '/dev/ttyUSB0' \
    --camera 2 \
    --name iphone_6s_back_camera \
    --iterations 300 \
    --type warm \
    --save \
    #2> error.txt