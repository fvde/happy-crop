#!/bin/bash

# sh predict.sh 192.168.178.48 1280 1280

host=${1}
width=${2}
height=${3}
brightness=0.1
confidence=0.5
file_name="latest.jpg"

ssh pi@$host << EOF
  libcamera-still --brightness $brightness --width $width --height $height -n -o $file_name
  yolo detect predict model=yolov8n.pt source=$file_name save=True imgsz=$width conf=$confidence save_txt=True
EOF

scp pi@$host:/home/pi/$file_name .