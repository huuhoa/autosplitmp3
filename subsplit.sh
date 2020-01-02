#!/bin/bash
for i in *.srt
do
    eval 'fbname=$(basename "$i" .srt)'
    python sub2track.py -s "$i" -t "$fbname.list" -p "$fbname"
    python split.py -ot "$fbname.mp3" -t "$fbname.list"
done
