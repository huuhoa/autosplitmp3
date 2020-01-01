#!/bin/bash
for i in *.srt
do
    eval 'fbname=$(basename "$i" .srt)'
    python sub2track.py "$i" "$fbname.list" "$fbname"
    python split.py "$fbname.mp3" "$fbname.list"
done
