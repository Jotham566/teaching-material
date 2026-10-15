#!/bin/sh
set -eu
TASK_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$TASK_DIR"
cat > .build/video-frames.txt <<'EOF'
file '../output/demo/01.png'
duration 8
file '../output/demo/02.png'
duration 8
file '../output/demo/03.png'
duration 7
file '../output/demo/04.png'
duration 8
file '../output/demo/05.png'
duration 9
file '../output/demo/05.png'
EOF
ffmpeg -y -v error -f concat -safe 0 -i .build/video-frames.txt -vf 'fps=30,tpad=stop_mode=clone:stop_duration=2,pad=1080:1920:0:285:color=0x002540,fade=t=in:st=0:d=0.4,format=yuv420p' -r 30 -t 40 -c:v libx264 -preset medium -crf 20 -movflags +faststart output/Sales_Data_Demo_40s.mp4
