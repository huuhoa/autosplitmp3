#!/bin/bash
for i in *.srt
do
    echo $(basename $i)
done

echo $1
python sub2track.py "$1.srt" "$1.list" "$1"
python split.py "$1.mp3" "$1.list"
