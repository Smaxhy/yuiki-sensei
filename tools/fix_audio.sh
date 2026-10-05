#!/bin/bash
# $1 = mp3 file. Ensure >=250 ms leading silence and peak about -1.5 dB (gain capped at +9 dB).
f="$1"
info=$(ffmpeg -hide_banner -nostats -i "$f" -af silencedetect=n=-45dB:d=0.01,volumedetect -f null - 2>&1)
mx=$(echo "$info" | grep -o "max_volume: [-0-9.]*" | awk '{print $2}')
lead=$(echo "$info" | grep -m1 "silence_end" | grep -o "silence_end: [0-9.]*" | awk '{print $2}')
first_start=$(echo "$info" | grep -m1 "silence_start" | grep -o "silence_start: [-0-9.]*" | awk '{print $2}')
# leading silence only counts if the first silence starts at 0
if [ -z "$lead" ] || [ "$(echo "$first_start > 0.001" | bc)" = 1 ]; then lead=0; fi
add=$(echo "x=(0.25-$lead)*1000; if (x<0) x=0; x" | bc | cut -d. -f1); add=${add:-0}
g=$(echo "x=-1.5-($mx); if (x>9) x=9; if (x<0) x=0; x" | bc)
if [ "$add" -lt 20 ] && [ "$(echo "$g < 1" | bc)" = 1 ]; then exit 0; fi
tmp="${f%.mp3}.tmp.mp3"
ffmpeg -hide_banner -loglevel error -y -i "$f" -af "adelay=delays=${add}:all=1,volume=${g}dB,alimiter=limit=0.89" -ar 24000 -ac 1 -b:a 48k "$tmp" && mv "$tmp" "$f"
